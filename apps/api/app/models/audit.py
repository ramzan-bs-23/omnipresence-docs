from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    """Immutable audit trail for all data changes."""

    ACTION_CHOICES = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )
    table_name = models.CharField(
        max_length=100,
        help_text='Table that was changed'
    )
    record_id = models.BigIntegerField(
        help_text='ID of the affected record'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES,
        help_text='Type of action performed'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs',
        help_text='User who made the change'
    )
    old_values = models.JSONField(
        null=True,
        blank=True,
        help_text='Previous values (for updates)'
    )
    new_values = models.JSONField(
        null=True,
        blank=True,
        help_text='New values'
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When change occurred'
    )
    source_device = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text='Device identifier'
    )

    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['table_name', 'record_id']),
            models.Index(fields=['changed_by']),
            models.Index(fields=['changed_at']),
            models.Index(fields=['-changed_at']),  # For sorting by newest first
        ]
        verbose_name_plural = 'Audit Logs'

    def __str__(self):
        return f"{self.action} on {self.table_name}:{self.record_id} by {self.changed_by}"

    def save(self, *args, **kwargs):
        # Prevent updates to audit logs (immutable)
        if self.pk:
            raise ValueError("Audit logs cannot be modified")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion of audit logs
        raise ValueError("Audit logs cannot be deleted")


class SyncConflict(models.Model):
    """Stores conflicting versions from offline sync."""

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='sync_conflicts'
    )
    session = models.ForeignKey(
        'Session',
        on_delete=models.CASCADE,
        related_name='sync_conflicts'
    )
    participant = models.ForeignKey(
        'Participant',
        on_delete=models.CASCADE,
        related_name='sync_conflicts'
    )
    version_a_data = models.JSONField(
        help_text='First version with metadata'
    )
    version_b_data = models.JSONField(
        help_text='Second version with metadata'
    )
    resolved_with_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text='ID of chosen resolution'
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Resolution timestamp'
    )
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='resolved_conflicts',
        help_text='User who resolved the conflict'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When conflict was detected'
    )

    class Meta:
        db_table = 'sync_conflicts'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['session']),
            models.Index(fields=['participant']),
            models.Index(fields=['resolved_with_id']),
            models.Index(fields=['resolved_at']),  # For filtering unresolved
        ]
        verbose_name_plural = 'Sync Conflicts'

    def __str__(self):
        status = "Resolved" if self.resolved_at else "Unresolved"
        return f"Conflict: {self.participant.full_name} in {self.session.name} ({status})"

    @property
    def is_resolved(self):
        """Check if conflict has been resolved."""
        return bool(self.resolved_at)

    @property
    def participant_name(self):
        """Get participant name for display."""
        return self.participant.full_name

    @property
    def session_name(self):
        """Get session name for display."""
        return self.session.name


class Notification(models.Model):
    """In-app notification queue."""

    NOTIFICATION_TYPE_CHOICES = [
        ('absence', 'Absence'),
        ('conflict', 'Conflict'),
        ('data_quality', 'Data Quality'),
        ('system', 'System'),
        ('info', 'Information'),
    ]

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text='Notification recipient'
    )
    notification_type = models.CharField(
        max_length=50,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='info',
        help_text='Type of notification'
    )
    title = models.CharField(
        max_length=255,
        help_text='Notification title'
    )
    message = models.TextField(
        help_text='Notification message'
    )
    link = models.CharField(
        max_length=500,
        null=True,
        blank=True,
        help_text='Optional link to related resource'
    )
    is_read = models.BooleanField(
        default=False,
        help_text='Read status'
    )
    read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='When marked as read'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When notification was created'
    )

    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['organization']),
            models.Index(fields=['user']),
            models.Index(fields=['is_read']),
            models.Index(fields=['-created_at']),  # For sorting by newest first
        ]
        verbose_name_plural = 'Notifications'

    def __str__(self):
        return f"{self.title} - {self.user.email}"

    def mark_as_read(self):
        """Mark notification as read."""
        from django.utils import timezone
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=['is_read', 'read_at'])

    def mark_as_unread(self):
        """Mark notification as unread."""
        self.is_read = False
        self.read_at = None
        self.save(update_fields=['is_read', 'read_at'])
