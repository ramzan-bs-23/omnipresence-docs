from django.db import models
from .base import TimeStampedModel


class Group(TimeStampedModel):
    """Logical collection of participants (class, room, session type, etc.)."""

    GROUP_TYPE_CHOICES = [
        ('class', 'Class'),
        ('room', 'Room'),
        ('session_type', 'Session Type'),
        ('department', 'Department'),
        ('team', 'Team'),
        ('other', 'Other'),
    ]

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text='Optional parent group for hierarchy'
    )
    name = models.CharField(max_length=255)
    group_type = models.CharField(
        max_length=50,
        choices=GROUP_TYPE_CHOICES,
        default='class',
        help_text='Type of group'
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Domain-specific configuration'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'groups'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['parent_id']),
            models.Index(fields=['group_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_group_type_display()})"

    @property
    def participant_count(self):
        """Get the number of participants in this group."""
        return self.memberships.count()


class GroupMembership(models.Model):
    """Many-to-many relationship between participants and groups."""

    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.CASCADE,
        related_name='memberships'
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Role or section within group'
    )

    class Meta:
        db_table = 'group_memberships'
        unique_together = [['group', 'participant']]
        indexes = [
            models.Index(fields=['group']),
            models.Index(fields=['participant']),
        ]

    def __str__(self):
        return f"{self.participant.full_name} in {self.group.name}"
