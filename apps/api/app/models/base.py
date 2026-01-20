from django.db import models
from django.contrib.auth.models import AbstractUser


class TimeStampedModel(models.Model):
    """Base model with organization scoping and timestamps."""

    organization = models.ForeignKey(
        'Organization',
        on_delete=models.CASCADE,
        related_name='%(class)ss',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """Custom user model for authentication."""

    ROLE_CHOICES = [
        ('frontline', 'Frontline User'),
        ('administrator', 'Administrator'),
        ('manager', 'Manager / Viewer'),
        ('external', 'External Participant'),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='frontline')
    is_active = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'users'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email
