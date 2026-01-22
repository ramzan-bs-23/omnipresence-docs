from django.db import models


class Organization(models.Model):
    """Organization/Domain for multi-tenancy."""

    DOMAIN_TYPE_CHOICES = [
        ('education', 'Education'),
        ('hospitality', 'Hospitality'),
        ('events', 'Events'),
        ('corporate', 'Corporate'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    domain = models.CharField(max_length=255, unique=True)
    domain_type = models.CharField(
        max_length=50,
        choices=DOMAIN_TYPE_CHOICES,
        default='education',
        help_text='Type of domain for terminology and configuration'
    )
    settings = models.JSONField(
        default=dict,
        blank=True,
        help_text='Domain-specific settings and terminology mappings'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'organizations'

    def __str__(self):
        return self.name
