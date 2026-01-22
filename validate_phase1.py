#!/usr/bin/env python3
"""
Quick validation script to check if Django models can be imported.
This helps verify Phase 1 implementation without running full migrations.
"""

import sys
import os

# Add the apps/api directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'apps', 'api'))

# Set Django settings module before importing models
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

def validate_imports():
    """Try to import all models to verify they're correctly defined."""
    print("=" * 60)
    print("PHASE 1: FOUNDATION - MODEL VALIDATION")
    print("=" * 60)

    models_to_check = [
        ('base', 'TimeStampModel, User'),
        ('organization', 'Organization'),
        ('participant', 'Participant'),
        ('group', 'Group, GroupMembership'),
        ('session', 'Session'),
        ('presence', 'PresenceState, PresenceRecord'),
        ('audit', 'AuditLog, SyncConflict, Notification'),
    ]

    errors = []
    successes = []

    for module_name, expected_classes in models_to_check:
        module_path = f'app.models.{module_name}'
        try:
            __import__(module_path)
            successes.append(f"✓ {module_path} - {expected_classes}")
        except ImportError as e:
            errors.append(f"✗ {module_path} - {e}")
        except Exception as e:
            errors.append(f"✗ {module_path} - Unexpected error: {e}")

    # Check permissions
    print("\n--- Permissions ---")
    try:
        from app.core.permissions import (
            IsFrontline, IsAdministrator, IsManager,
            IsAdministratorOrManager, IsExternal
        )
        successes.append("✓ app.core.permissions - All permission classes")
    except ImportError as e:
        errors.append(f"✗ app.core.permissions - {e}")
    except Exception as e:
        errors.append(f"✗ app.core.permissions - Unexpected error: {e}")

    # Check auth views
    print("\n--- Authentication Views ---")
    try:
        from app.api.views import auth
        if hasattr(auth, 'login_view'):
            successes.append("✓ app.api.views.auth - login_view")
        if hasattr(auth, 'logout_view'):
            successes.append("✓ app.api.views.auth - logout_view")
        if hasattr(auth, 'me_view'):
            successes.append("✓ app.api.views.auth - me_view")
    except ImportError as e:
        errors.append(f"✗ app.api.views.auth - {e}")
    except Exception as e:
        errors.append(f"✗ app.api.views.auth - Unexpected error: {e}")

    # Check middleware
    print("\n--- Middleware ---")
    try:
        from app.core.middleware import OrganizationMiddleware
        successes.append("✓ app.core.middleware - OrganizationMiddleware")
    except ImportError as e:
        errors.append(f"✗ app.core.middleware - {e}")
    except Exception as e:
        errors.append(f"✗ app.core.middleware - Unexpected error: {e}")

    # Print results
    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)

    print(f"\nSuccessful imports ({len(successes)}):")
    for success in successes:
        print(f"  {success}")

    if errors:
        print(f"\nFailed imports ({len(errors)}):")
        for error in errors:
            print(f"  {error}")

    print("\n" + "=" * 60)

    if errors:
        print(f"STATUS: {len(errors)} error(s) found")
        print("\nNOTE: Some errors are expected if Django/dependencies are not installed.")
        print("To fully test, run:")
        print("  cd apps/api")
        print("  pip install -r requirements.txt")
        print("  python manage.py makemigrations")
        print("  python manage.py migrate")
        print("  python manage.py check")
        return 1
    else:
        print("STATUS: All imports successful!")
        return 0

if __name__ == '__main__':
    sys.exit(validate_imports())
