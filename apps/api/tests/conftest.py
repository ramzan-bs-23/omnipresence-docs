"""
Pytest configuration and fixtures for Omnipresence tests.
"""
import pytest
from django.utils import timezone
from django.contrib.auth import get_user_model
from app.models import Organization


@pytest.fixture
def db_setup(db):
    """Set up test database with organization and user."""
    User = get_user_model()

    org = Organization.objects.create(
        name='Test Organization',
        slug='test-org',
        domain_type='education',
    )

    user = User.objects.create_user(
        email='admin@test.com',
        password='testpass123',
        role='administrator',
        organization=org,
    )

    return {'org': org, 'user': user}


@pytest.fixture
def authenticated_client(db, db_setup):
    """Return an authenticated client."""
    from django.test import Client

    client = Client()
    client.force_login(db_setup['user'])
    return client


@pytest.fixture
def api_client(authenticated_client):
    """Return an API client with authentication."""
    return authenticated_client
