from django.db import models
from .base import TimeStampedModel


class PresenceState(TimeStampedModel):
    """Configurable presence states (present, absent, late, etc.)."""

    DOMAIN_CHOICES = [
        ('education', 'Education'),
        ('hospitality', 'Hospitality'),
        ('events', 'Events'),
        ('corporate', 'Corporate'),
    ]

    domain = models.CharField(
        max_length=50,
        choices=DOMAIN_CHOICES,
        help_text='Domain this state applies to'
    )
    code = models.CharField(
        max_length=50,
        help_text='State code (e.g., "present", "absent", "late")'
    )
    label = models.CharField(
        max_length=100,
        help_text='Display label for this state'
    )
    color = models.CharField(
        max_length=7,
        default='#00ff00',
        help_text='Hex color for UI display'
    )
    sort_order = models.IntegerField(
        default=0,
        help_text='Display order'
    )
    is_default = models.BooleanField(
        default=False,
        help_text='Whether this is a default state'
    )

    class Meta:
        db_table = 'presence_states'
        unique_together = [['organization', 'domain', 'code']]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['domain']),
        ]

    def __str__(self):
        return f"{self.label} ({self.code})"

    @classmethod
    def get_default_states(cls, organization, domain):
        """Get default presence states for a domain."""
        from django.core.cache import cache

        cache_key = f"default_states_{organization.id}_{domain}"
        cached = cache.get(cache_key)
        if cached:
            return cached

        # Create default states if they don't exist
        default_configs = {
            'education': [
                ('present', 'Present', '#22c55e', 0),
                ('absent', 'Absent', '#ef4444', 1),
                ('late', 'Late', '#f59e0b', 2),
                ('excused', 'Excused', '#3b82f6', 3),
            ],
            'hospitality': [
                ('present', 'Checked In', '#22c55e', 0),
                ('absent', 'Not Arrived', '#ef4444', 1),
                ('checked_out', 'Checked Out', '#6b7280', 2),
            ],
            'events': [
                ('present', 'Attended', '#22c55e', 0),
                ('absent', 'No Show', '#ef4444', 1),
                ('partial', 'Partial', '#f59e0b', 2),
            ],
            'corporate': [
                ('present', 'Present', '#22c55e', 0),
                ('absent', 'Absent', '#ef4444', 1),
                ('remote', 'Remote', '#3b82f6', 2),
                ('late', 'Late', '#f59e0b', 3),
            ],
        }

        states = []
        for code, label, color, sort_order in default_configs.get(domain, []):
            state, created = cls.objects.get_or_create(
                organization=organization,
                domain=domain,
                code=code,
                defaults={
                    'label': label,
                    'color': color,
                    'sort_order': sort_order,
                    'is_default': True
                }
            )
            states.append(state)

        cache.set(cache_key, states, timeout=3600)
        return states


class PresenceRecord(TimeStampedModel):
    """Attendance record linking participant to session with status."""

    session = models.ForeignKey(
        'Session',
        on_delete=models.CASCADE,
        related_name='presence_records',
        help_text='Session for this presence record'
    )
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.CASCADE,
        related_name='presence_records',
        help_text='Participant whose presence is recorded'
    )
    presence_state = models.ForeignKey(
        'PresenceState',
        on_delete=models.PROTECT,
        help_text='Presence state (present, absent, etc.)'
    )
    recorded_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When presence was recorded'
    )
    recorded_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_presence',
        help_text='User who recorded this presence'
    )
    source_device_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Device identifier for sync conflicts'
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Additional notes or metadata'
    )

    class Meta:
        db_table = 'presence_records'
        unique_together = [['session', 'participant']]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['session']),
            models.Index(fields=['participant']),
            models.Index(fields=['recorded_at']),
        ]

    def __str__(self):
        return f"{self.participant.full_name} - {self.session.name} - {self.presence_state.label}"

    def save(self, *args, **kwargs):
        # Trigger audit log on create/update
        from .audit import AuditLog
        from django.utils import timezone

        is_new = self.pk is None
        old_state = None

        if not is_new:
            try:
                old_record = PresenceRecord.objects.get(pk=self.pk)
                old_state = old_record.presence_state
            except PresenceRecord.DoesNotExist:
                pass

        super().save(*args, **kwargs)

        # Create audit log
        if is_new:
            AuditLog.objects.create(
                organization=self.organization,
                table_name='presence_records',
                record_id=self.pk,
                action='create',
                changed_by=self.recorded_by,
                new_values={
                    'session_id': self.session_id,
                    'participant_id': self.participant_id,
                    'presence_state': self.presence_state.code
                },
                changed_at=timezone.now(),
                source_device=self.source_device_id
            )
        elif old_state and old_state != self.presence_state:
            AuditLog.objects.create(
                organization=self.organization,
                table_name='presence_records',
                record_id=self.pk,
                action='update',
                changed_by=self.recorded_by,
                old_values={'presence_state': old_state.code},
                new_values={'presence_state': self.presence_state.code},
                changed_at=timezone.now(),
                source_device=self.source_device_id
            )
