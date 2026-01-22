from django.db import models
from .base import TimeStampedModel


class Session(TimeStampedModel):
    """Time-bound event where presence is recorded."""

    group = models.ForeignKey(
        'Group',
        on_delete=models.CASCADE,
        related_name='sessions',
        help_text='Group associated with this session'
    )
    name = models.CharField(max_length=255)
    scheduled_start_at = models.DateTimeField(help_text='Scheduled start time')
    scheduled_end_at = models.DateTimeField(help_text='Scheduled end time')
    actual_start_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Actual start time (when session began)'
    )
    actual_end_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Actual end time (when session ended)'
    )
    location = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text='Physical or virtual location'
    )
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Domain-specific session data'
    )

    class Meta:
        db_table = 'sessions'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['group']),
            models.Index(fields=['scheduled_start_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.scheduled_start_at.strftime('%Y-%m-%d %H:%M')})"

    @property
    def is_in_progress(self):
        """Check if session is currently in progress."""
        from django.utils import timezone
        now = timezone.now()
        return (
            self.actual_start_at and
            not self.actual_end_at and
            now >= self.actual_start_at
        )

    @property
    def is_completed(self):
        """Check if session has ended."""
        return bool(self.actual_end_at)

    @property
    def is_scheduled(self):
        """Check if session is scheduled but not started."""
        return not bool(self.actual_start_at)

    @property
    def presence_stats(self):
        """Get presence statistics for this session."""
        records = self.presence_records.all()
        total = records.count()
        if total == 0:
            return {'total': 0, 'present': 0, 'absent': 0}

        present = records.filter(presence_state__code='present').count()
        return {
            'total': total,
            'present': present,
            'absent': total - present
        }
