from django.db import models
from .base import TimeStampedModel


class Participant(TimeStampedModel):
    """Individual whose presence is tracked (student, guest, attendee, etc.)."""

    external_id = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='External system reference (optional)'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identifier = models.CharField(
        max_length=100,
        help_text='Student ID, badge number, etc.'
    )
    date_of_birth = models.DateField(null=True, blank=True)
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        help_text='Domain-specific additional data'
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'participants'
        unique_together = [['organization', 'identifier']]
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.identifier})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
