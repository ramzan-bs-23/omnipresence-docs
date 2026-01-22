# Omnipresence Implementation Plan

## Project Overview

**Omnipresence** is a unified presence and attendance management platform for education, hospitality, events, and
corporate environments. The system enables organizations to reliably mark, track, and understand "who was present,
where, and when" with minimal user effort.

### Tech Stack

- **Backend**: Django REST Framework 5.0+ with Python 3.11+
- **Frontend**: React 18+ with Vite 5+, TypeScript, Zustand
- **Database**: MySQL 8.0+
- **Deployment**: Docker + Docker Compose

### Current Status

- ✅ Project structure scaffolded
- ✅ Basic Django settings configured
- ✅ Base models (User, Organization) created
- ✅ Core middleware/permissions skeleton
- ✅ React app with Vite setup
- ⚠️ **Most features not yet implemented**

---

## User Decisions

**Implementation Scope:** All phases sequentially (1-8)
**Authentication Method:** Session-based authentication (Django built-in)

---

## Phase 1: Foundation (Weeks 1-2) - START HERE

### 1.1 Complete Database Models (WP-001)

**Files to create:**

- `apps/api/app/models/participant.py`
- `apps/api/app/models/group.py`
- `apps/api/app/models/session.py`
- `apps/api/app/models/presence.py`
- `apps/api/app/models/audit.py`

**Models to implement:**

#### Participant Model

```python
# apps/api/app/models/participant.py
from django.db import models
from .base import TimeStampedModel


class Participant(TimeStampedModel):
    external_id = models.CharField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'participants'
        unique_together = [['organization', 'identifier']]
```

#### Group Models

```python
# apps/api/app/models/group.py
from django.db import models
from .base import TimeStampedModel


class Group(TimeStampedModel):
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    group_type = models.CharField(max_length=50)
    extra_data = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'groups'


class GroupMembership(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'group_memberships'
        unique_together = [['group', 'participant']]
```

#### Session Model

```python
# apps/api/app/models/session.py
from django.db import models
from .base import TimeStampedModel


class Session(TimeStampedModel):
    group = models.ForeignKey('Group', on_delete=models.CASCADE, related_name='sessions')
    name = models.CharField(max_length=255)
    scheduled_start_at = models.DateTimeField()
    scheduled_end_at = models.DateTimeField()
    actual_start_at = models.DateTimeField(null=True, blank=True)
    actual_end_at = models.DateTimeField(null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'sessions'
```

#### Presence Models

```python
# apps/api/app/models/presence.py
from django.db import models
from .base import TimeStampedModel


class PresenceState(TimeStampedModel):
    domain = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    label = models.CharField(max_length=100)
    color = models.CharField(max_length=7)
    sort_order = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = 'presence_states'
        unique_together = [['organization', 'domain', 'code']]


class PresenceRecord(TimeStampedModel):
    session = models.ForeignKey('Session', on_delete=models.CASCADE, related_name='presence_records')
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='presence_records')
    presence_state = models.ForeignKey('PresenceState', on_delete=models.PROTECT)
    recorded_at = models.DateTimeField(auto_now_add=True)
    recorded_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    source_device_id = models.CharField(max_length=100, null=True, blank=True)
    extra_data = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'presence_records'
        unique_together = [['session', 'participant']]
```

#### Audit & Sync Models

```python
# apps/api/app/models/audit.py
from django.db import models
from django.conf import settings


class AuditLog(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    table_name = models.CharField(max_length=100)
    record_id = models.BigIntegerField()
    action = models.CharField(max_length=20)  # create, update, delete
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    old_values = models.JSONField(null=True, blank=True)
    new_values = models.JSONField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    source_device = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'audit_logs'
        indexes = [
            models.Index(fields=['table_name', 'record_id']),
            models.Index(fields=['changed_by']),
            models.Index(fields=['changed_at']),
        ]


class SyncConflict(models.Model):
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    session = models.ForeignKey('Session', on_delete=models.CASCADE)
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE)
    version_a_data = models.JSONField()
    version_b_data = models.JSONField()
    resolved_with_id = models.BigIntegerField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sync_conflicts'


class Notification(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    message = models.TextField()
    link = models.CharField(max_length=500, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
```

**Update models/__init__.py:**

```python
# apps/api/app/models/__init__.py
from .base import TimeStampedModel, User
from .organization import Organization
from .participant import Participant
from .group import Group, GroupMembership
from .session import Session
from .presence import PresenceState, PresenceRecord
from .audit import AuditLog, SyncConflict, Notification
```

**Run migrations:**

```bash
cd apps/api
python manage.py makemigrations
python manage.py migrate
```

### 1.2 Authentication System (WP-002)

**Files to create:**

- `apps/api/app/api/views/auth.py` - Login/logout views
- `apps/api/app/api/serializers/auth.py` - Auth serializers
- `apps/api/app/services/auth_service.py` - Business logic

**Authentication Views:**

```python
# apps/api/app/api/views/auth.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from drf_spectacular.utils import extend_schema


@api_view(['POST'])
@permission_classes([AllowAny])
@extend_schema(tags=['Authentication'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, username=email, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'role': user.role,
                    'organization': {
                        'id': user.organization.id,
                        'name': user.organization.name,
                    }
                }
            }
        })
    return Response({
        'errors': [{'message': 'Invalid credentials'}]
    }, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@extend_schema(tags=['Authentication'])
def logout_view(request):
    logout(request)
    return Response({'data': {'success': True}})
```

**Update API URLs:**

```python
# apps/api/app/api/urls.py
from django.urls import path
from .views import auth

urlpatterns = [
    path('auth/login/', auth.login_view, name='login'),
    path('auth/logout/', auth.logout_view, name='logout'),
]
```

### 1.3 Multi-Tenancy Middleware (WP-003)

**IMPORTANT:** OrganizationMiddleware already implemented in `apps/api/app/core/middleware.py`

**Just add to settings.py MIDDLEWARE:**

```python
MIDDLEWARE = [
    # ... existing middleware ...
    'app.core.middleware.OrganizationMiddleware',
]
```

**Organization scoping to add:**

- Create organization settings storage (JSON field on Organization model)
- Implement organization user scoping (users see only their org data)
- Add organization_id filtering to all queries (via manager methods)

### 1.4 Role-Based Access Control (WP-002 - Additional)

**IMPORTANT:** Permission classes already exist in `apps/api/app/core/permissions.py`:

- `IsFrontline` - Frontline users only
- `IsAdministrator` - Administrators only
- `IsManager` - Managers/Viewers only
- `IsAdministratorOrManager` - Admins and Managers

**Additional needed:**

```python
# Add to apps/api/app/core/permissions.py
class IsExternal(permissions.BasePermission):
    """Allows access only to external participants."""

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role == 'external'
```

**Session management (WP-002):**

- Implement configurable session expiration
- Add SESSION_COOKIE_AGE to settings.py
- Add last_login_at tracking on User model (already exists)

---

## Phase 2: Core CRUD Features (Weeks 3-4)

### 2.1 Participant & Group Management (WP-004)

**Files to create:**

- `apps/api/app/api/views/participants.py`
- `apps/api/app/api/views/groups.py`
- `apps/api/app/api/serializers/participants.py`
- `apps/api/app/api/serializers/groups.py`
- `apps/api/app/services/participant_service.py`

**Endpoints:**

- GET/POST `/api/participants/` - List/create participants
- GET/PUT `/api/participants/{id}/` - Detail/update
- POST `/api/participants/bulk/` - CSV import
- GET/POST `/api/groups/` - List/create groups
- GET/PUT/DELETE `/api/groups/{id}/` - Detail/update/delete
- POST `/api/groups/{id}/members/` - Add participants to group

### 2.2 Session Management (WP-005)

**Files to create:**

- `apps/api/app/api/views/sessions.py`
- `apps/api/app/api/serializers/sessions.py`
- `apps/api/app/services/session_service.py`

**Endpoints:**

- GET/POST `/api/sessions/` - List/create sessions
- GET/PUT `/api/sessions/{id}/` - Detail/update
- PATCH `/api/sessions/{id}/start/` - Mark session started
- PATCH `/api/sessions/{id}/end/` - Mark session ended

### 2.3 Presence Recording (WP-006)

**Files to create:**

- `apps/api/app/api/views/presence.py`
- `apps/api/app/api/serializers/presence.py`
- `apps/api/app/services/presence_service.py`

**Endpoints:**

- GET `/api/presence/` - List presence records
- POST `/api/presence/` - Record presence (single/bulk)
- PUT `/api/presence/{id}/` - Update presence record
- POST `/api/presence/sync/` - Offline sync endpoint

### 2.4 Domain Configuration (WP-007)

**Files to create:**

- `apps/api/app/api/views/admin.py` - Admin endpoints
- `apps/api/app/api/serializers/admin.py`
- `apps/api/app/services/domain_service.py` - Domain configuration logic

**Organization model needs additional fields:**

```python
# Add to Organization model
domain_type = models.CharField(max_length=50)  # 'education', 'hospitality', 'events', 'corporate'
settings = models.JSONField(default=dict, blank=True)  # Domain-specific settings
```

**Endpoints:**

- GET `/api/admin/presence-states/` - List configured states
- POST `/api/admin/presence-states/` - Create custom state
- GET `/api/admin/domain-config/` - Get domain configuration
- PUT `/api/admin/domain-config/` - Update domain settings

**Domain terminology mapping:**

- Create domain-specific label mappings (e.g., "student" vs "guest" vs "attendee")
- Store in Organization.settings
- Use in UI for dynamic labels

---

## Phase 3: Frontend UI (Weeks 5-6)

### 3.1 Core Components

**Files to create:**

- `apps/web/src/components/common/Button.tsx`
- `apps/web/src/components/common/Input.tsx`
- `apps/web/src/components/common/Select.tsx`
- `apps/web/src/components/common/Table.tsx`
- `apps/web/src/components/common/Modal.tsx`
- `apps/web/src/components/common/Toast.tsx`

### 3.2 Layout Components

**Files to create:**

- `apps/web/src/components/layout/Header.tsx`
- `apps/web/src/components/layout/Sidebar.tsx`
- `apps/web/src/components/layout/MainLayout.tsx`

### 3.3 Auth Pages

**Files to create:**

- `apps/web/src/pages/LoginPage.tsx`
- Update `apps/web/src/store/auth.ts` - Enhance with login actions

### 3.4 Participant & Group Pages

**Files to create:**

- `apps/web/src/pages/participants/ParticipantListPage.tsx`
- `apps/web/src/pages/participants/ParticipantDetailPage.tsx`
- `apps/web/src/pages/groups/GroupListPage.tsx`
- `apps/web/src/pages/groups/GroupDetailPage.tsx`

### 3.5 Session Pages

**Files to create:**

- `apps/web/src/pages/sessions/SessionListPage.tsx`
- `apps/web/src/pages/sessions/SessionDetailPage.tsx`
- `apps/web/src/pages/sessions/PresenceRecordingPage.tsx` - Quick toggle UI

### 3.6 Offline Storage (WP-010)

**Files to create:**

- `apps/web/src/utils/offlineStorage.ts` - IndexedDB wrapper
- `apps/web/src/hooks/useOfflineSync.ts` - Sync hook
- `apps/web/src/hooks/useOnlineStatus.ts` - Connection status detection

**IndexedDB schema:**

- Store: `presence_records` - Offline presence records
- Store: `sync_queue` - Pending sync operations
- Store: `participants_cache` - Cached participant data
- Store: `sessions_cache` - Cached session data

**Connection status detection:**

- Use `navigator.onLine` API
- Add event listeners for `online` and `offline` events
- Show UI indicator for connection status
- Auto-trigger sync when connection restored

### 3.7 Manual Data Entry UI (WP-008)

**Files to create:**

- `apps/web/src/pages/sessions/PresenceRecordingPage.tsx` - Main recording interface
- `apps/web/src/components/presence/ParticipantList.tsx` - List with toggle buttons
- `apps/web/src/components/presence/PresenceToggle.tsx` - Quick toggle component
- `apps/web/src/components/presence/BulkMarkPresent.tsx` - "Mark all present" action
- `apps/web/src/components/presence/QuickAddParticipant.tsx` - On-the-spot participant creation

**Features:**

- Session detail page with participant list
- Quick toggle buttons (present/absent/states)
- Bulk "mark all present" action
- On-the-spot participant creation
- Form validation and error handling
- Auto-save to prevent data loss

### 3.8 Bulk Data Import UI (WP-009)

**Files to create:**

- `apps/web/src/components/import/CSVUploader.tsx` - File upload component
- `apps/web/src/components/import/ImportProgress.tsx` - Progress indicator
- `apps/web/src/components/import/ImportErrors.tsx` - Error display

**Features:**

- CSV file upload endpoint
- CSV parsing and validation
- Error reporting for invalid rows
- Import progress tracking
- Support for participants and groups import

### 3.9 External Participant Portal (WP-011) - OPTIONAL

**Files to create:**

- `apps/web/src/pages/external/ExternalSubmitPage.tsx` - Self-service form
- `apps/web/src/pages/external/ExternalConfirmationPage.tsx` - Confirmation display
- `apps/web/src/pages/external/ExternalDataPage.tsx` - Limited read-only access

**Features:**

- Secure access for external participants
- Presence submission form
- Confirmation display
- Limited read-only access to own data
- Special token-based authentication for external users

---

## Phase 4: Offline Sync (Weeks 7-8)

### 4.1 Sync Conflict Detection (WP-012)

**Files to create:**

- `apps/api/app/services/sync_service.py`

**Functionality:**

- Compare client vs server records
- Detect conflicts for same participant+session
- Create SyncConflict records
- Return sync results with conflicts

### 4.2 Conflict Resolution UI (WP-013)

**Files to create:**

- `apps/web/src/pages/admin/ConflictListPage.tsx`
- `apps/web/src/components/admin/ConflictResolver.tsx`
- `apps/web/src/components/admin/SideBySideComparison.tsx` - Version comparison

**Endpoints:**

- GET `/api/admin/sync-conflicts/` - List conflicts
- POST `/api/admin/sync-conflicts/{id}/resolve/` - Resolve conflict

**Features:**

- Conflict list view for administrators
- Side-by-side comparison of versions
- Manual resolution interface (choose server or client version)
- Resolution audit logging
- Bulk resolution actions

### 4.3 Sync History Management (WP-014)

**Files to create:**

- `apps/api/app/models/sync_history.py` - Sync history tracking model
- `apps/api/app/api/views/sync_history.py` - Sync history endpoints
- `apps/web/src/pages/admin/SyncHistoryPage.tsx` - Sync history display

**Model to add:**

```python
# apps/api/app/models/sync_history.py
class SyncHistory(TimeStampedModel):
    device_id = models.CharField(max_length=100)
    synced_at = models.DateTimeField(auto_now_add=True)
    records_synced = models.IntegerField()
    conflicts_created = models.IntegerField()
    status = models.CharField(max_length=20)  # 'success', 'partial', 'failed'
    error_message = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'sync_history'
```

**Endpoints:**

- GET `/api/admin/sync-history/` - List sync operations
- GET `/api/admin/sync-history/{id}/` - Sync operation details
- POST `/api/admin/sync-history/{id}/retry/` - Retry failed sync

**Features:**

- Store sync batch history
- Track device IDs and sync timestamps
- Sync status indicators
- Retry mechanism for failed syncs

---

## Phase 5: Reporting (Weeks 9-10)

### 5.1 Report Generation (WP-015)

**Files to create:**

- `apps/api/app/services/report_service.py`
- `apps/api/app/api/views/reports.py`
- `apps/web/src/pages/reports/ReportListPage.tsx`
- `apps/web/src/pages/reports/AttendanceReportPage.tsx`
- `apps/web/src/components/reports/ReportFilters.tsx`

**Endpoints:**

- GET `/api/reports/attendance/` - Attendance report
- GET `/api/reports/absentees/` - Absentee list
- GET `/api/reports/summary/` - Operational summaries

**Features:**

- Operational summaries (daily, by session)
- Aggregate reports (weekly, monthly, custom ranges)
- Report filters: group, date range, presence state
- Report caching for performance (using Django cache framework)
- Report scheduling (optional - use Celery for async)

### 5.2 CSV Export (WP-016)

**Files to create:**

- `apps/api/app/utils/export.py` - CSV generation
- GET `/api/reports/export/{report_id}/` - Download CSV

### 5.3 PDF Export (WP-017)

**Files to create:**

- `apps/api/app/utils/pdf_generator.py` - PDF generation
- Add PDF format to export endpoint

---

## Phase 6: Notifications & Governance (Weeks 11-12)

### 6.1 Notification System (WP-018)

**Files to create:**

- `apps/api/app/services/notification_service.py`
- `apps/api/app/api/views/notifications.py`
- `apps/web/src/components/notifications/NotificationBell.tsx`
- `apps/web/src/components/notifications/NotificationList.tsx`
- `apps/web/src/pages/admin/NotificationRulesPage.tsx`

**Endpoints:**

- GET `/api/notifications/` - List notifications
- PATCH `/api/notifications/{id}/read/` - Mark read
- PATCH `/api/notifications/read-all/` - Mark all read
- GET `/api/admin/notification-rules/` - List notification rules
- POST `/api/admin/notification-rules/` - Create notification rule
- GET `/api/admin/notification-preferences/` - Get user preferences
- PUT `/api/admin/notification-preferences/` - Update preferences

**Features:**

- Notification creation API
- Notification list endpoint
- Mark as read/unread
- Notification rules engine (absent participants, conflicts, data quality)
- User notification preferences (per user)
- In-app notification bell/icon with unread count

### 6.2 Audit Logging (WP-019)

**Files to create:**

- `apps/api/app/services/audit_service.py`
- `apps/web/src/pages/admin/AuditLogPage.tsx`
- `apps/api/app/api/views/audit.py` - Audit log endpoints

**Endpoints:**

- GET `/api/admin/audit-logs/` - List audit logs with filters
- POST `/api/admin/audit-logs/export/` - Export audit logs (CSV)

**Features:**

- Automatic logging of all presence record changes
- Log: who, what, when, previous value, new value, source
- Audit log query endpoint (with filters: table_name, record_id, date_from, date_to, changed_by)
- Audit log export (CSV)
- Immutable log storage (no updates/deletes)

### 6.3 Data Retention (WP-020)

**Files to create:**

- `apps/api/app/management/commands/retention.py` - Django management command
- `apps/api/app/services/retention_service.py` - Retention logic
- `apps/api/app/models/retention_config.py` - Retention configuration model

**Retention Config Model:**

```python
# apps/api/app/models/retention_config.py
class RetentionConfig(TimeStampedModel):
    presence_records_years = models.IntegerField(default=3)
    audit_logs_years = models.IntegerField(default=1)
    organization_anonymize_days = models.IntegerField(default=90)

    class Meta:
        db_table = 'retention_config'
```

**Django management command:**

```bash
python manage.py retention --dry-run  # Preview what would be deleted
python manage.py retention --execute   # Execute retention cleanup
```

**Features:**

- Presence record retention (3 years minimum, configurable)
- Audit log retention (1 year)
- Soft delete for organizations (90-day anonymization)
- Retention configuration per organization
- Dry-run mode before executing cleanup

---

## Phase 7: Testing (Weeks 13-14)

### 7.1 Backend Tests (WP-021)

**Files to create:**

- `apps/api/tests/test_models.py` - Model tests
- `apps/api/tests/test_views/auth.py` - Auth view tests
- `apps/api/tests/test_views/participants.py` - Participant view tests
- `apps/api/tests/test_views/groups.py` - Group view tests
- `apps/api/tests/test_views/sessions.py` - Session view tests
- `apps/api/tests/test_views/presence.py` - Presence view tests
- `apps/api/tests/test_views/admin.py` - Admin view tests
- `apps/api/tests/test_services/` - Service layer tests
- `apps/api/tests/test_multi_tenancy.py` - Multi-tenancy isolation tests
- `apps/api/tests/test_sync_conflicts.py` - Sync conflict scenario tests

**Coverage target:** 80%+

**pytest.ini configuration:**

```ini
[pytest]
DJANGO_SETTINGS_MODULE = app.settings
python_files = test_*.py
python_classes = Test*
python_functions = test_*
--cov = apps
--cov-report = html
--cov-report = term
```

### 7.2 Frontend Tests (WP-022)

**Files to create:**

- `apps/web/src/components/common/*.test.tsx` - Common component tests
- `apps/web/src/components/layout/*.test.tsx` - Layout component tests
- `apps/web/src/components/presence/*.test.tsx` - Presence component tests
- `apps/web/src/components/import/*.test.tsx` - Import component tests
- `apps/web/src/pages/auth/*.test.tsx` - Auth page tests
- `apps/web/src/pages/participants/*.test.tsx` - Participant page tests
- `apps/web/src/pages/groups/*.test.tsx` - Group page tests
- `apps/web/src/pages/sessions/*.test.tsx` - Session page tests
- `apps/web/src/pages/admin/*.test.tsx` - Admin page tests
- `apps/web/src/utils/offlineStorage.test.ts` - Offline storage tests
- `apps/web/src/hooks/*.test.ts` - Hook tests
- `apps/web/tests/api/*.test.ts` - API client tests
- `apps/web/tests/e2e/` - E2E tests with Playwright

**Coverage target:** 70%+

**E2E test scenarios:**

- Login/logout flow
- Create participant and group
- Record presence for a session
- Sync offline data
- Generate and export report
- Resolve sync conflict

### 7.3 Performance Testing (WP-023)

**Files to create:**

- `apps/api/tests/performance/test_presence_recording.py` - Presence recording performance
- `apps/api/tests/performance/test_report_generation.py` - Report generation performance
- `apps/api/tests/performance/test_concurrent_users.py` - Concurrent user test
- `apps/api/tests/performance/test_large_groups.py` - Large group test
- `apps/api/tests/performance/test_sync_performance.py` - Sync performance test

**Tools to use:**

- pytest-benchmark for backend performance tests
- Locust or pytest-xdist for load testing
- Playwright for frontend performance metrics

**Targets:**

- Presence recording < 3 seconds
- Report generation < 10 seconds
- 50+ concurrent users
- 500+ participant groups
- Sync < 30 seconds

---

## Phase 8: Deployment (Week 15)

### 8.1 Production Setup (WP-024)

**Files to modify:**

- `docker-compose.yml` - Production configuration
- `infrastructure/docker/api.Dockerfile` - Backend container
- `infrastructure/docker/web.Dockerfile` - Frontend container
- `infrastructure/docker/nginx.conf` - Reverse proxy config
- `.env.production` - Production environment variables
- `infrastructure/docker/mysql.Dockerfile` - MySQL container config

**Production database configuration:**

```yaml
# docker-compose.yml (production)
services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./infrastructure/mysql/my.cnf:/etc/mysql/conf.d/custom.cnf
    restart: always
```

**SSL/HTTPS setup:**

- Use Let's Encrypt with certbot
- Configure nginx with SSL certificates
- Set up SSL renewal cron job

**Backup strategy:**

```bash
# Daily backup script
#!/bin/bash
# Backup MySQL database
docker exec mysql mysqldump -u root -p${MYSQL_ROOT_PASSWORD} omnipresence > backup_$(date +%Y%m%d).sql
# Backup to remote storage
aws s3 cp backup_$(date +%Y%m%d).sql s3://omnipresence-backups/
```

**Environment variable management:**

- Use `.env.production` for production
- Never commit production secrets
- Use AWS Secrets Manager or similar for secrets

**Deployment documentation to create:**

- `docs/deployment.md` - Deployment guide
- `docs/monitoring.md` - Monitoring and alerting setup
- `docs/troubleshooting.md` - Common issues and solutions

---

## Critical Files Summary

### Backend Files to Create/Modify:

**Models (Phase 1):**

1. `apps/api/app/models/participant.py` - NEW
2. `apps/api/app/models/group.py` - NEW
3. `apps/api/app/models/session.py` - NEW
4. `apps/api/app/models/presence.py` - NEW
5. `apps/api/app/models/audit.py` - NEW
6. `apps/api/app/models/sync_history.py` - NEW
7. `apps/api/app/models/retention_config.py` - NEW
8. `apps/api/app/models/__init__.py` - MODIFY
9. `apps/api/app/models/organization.py` - MODIFY (add domain_type, settings)

**Authentication & Permissions (Phase 1):**

10. `apps/api/app/api/views/auth.py` - NEW
11. `apps/api/app/api/serializers/auth.py` - NEW
12. `apps/api/app/api/urls.py` - MODIFY
13. `apps/api/app/core/middleware.py` - MODIFY (already exists, just add to settings)
14. `apps/api/app/core/permissions.py` - MODIFY (add IsExternal)
15. `apps/api/app/settings.py` - MODIFY (add middleware, session config)

**API Views (Phase 2):**

16. `apps/api/app/api/views/participants.py` - NEW
17. `apps/api/app/api/views/groups.py` - NEW
18. `apps/api/app/api/views/sessions.py` - NEW
19. `apps/api/app/api/views/presence.py` - NEW
20. `apps/api/app/api/views/admin.py` - NEW
21. `apps/api/app/api/views/reports.py` - NEW
22. `apps/api/app/api/views/notifications.py` - NEW
23. `apps/api/app/api/views/audit.py` - NEW

**Serializers (Phase 2):**

24. `apps/api/app/api/serializers/participants.py` - NEW
25. `apps/api/app/api/serializers/groups.py` - NEW
26. `apps/api/app/api/serializers/sessions.py` - NEW
27. `apps/api/app/api/serializers/presence.py` - NEW
28. `apps/api/app/api/serializers/admin.py` - NEW

**Services (Phase 2-6):**

29. `apps/api/app/services/auth_service.py` - NEW
30. `apps/api/app/services/participant_service.py` - NEW
31. `apps/api/app/services/session_service.py` - NEW
32. `apps/api/app/services/presence_service.py` - NEW
33. `apps/api/app/services/sync_service.py` - NEW
34. `apps/api/app/services/domain_service.py` - NEW
35. `apps/api/app/services/report_service.py` - NEW
36. `apps/api/app/services/notification_service.py` - NEW
37. `apps/api/app/services/audit_service.py` - NEW
38. `apps/api/app/services/retention_service.py` - NEW

**Tests (Phase 7):**

39. `apps/api/tests/test_models.py` - NEW
40. `apps/api/tests/test_views/*.py` - NEW (multiple files)
41. `apps/api/tests/test_services/*.py` - NEW (multiple files)
42. `apps/api/tests/test_multi_tenancy.py` - NEW
43. `apps/api/tests/test_sync_conflicts.py` - NEW
44. `apps/api/tests/performance/*.py` - NEW (multiple files)
45. `apps/api/pytest.ini` - NEW

**Management Commands (Phase 6):**

46. `apps/api/app/management/commands/retention.py` - NEW

### Frontend Files to Create/Modify:

**Core (Phase 3):**

47. `apps/web/src/components/common/Button.tsx` - NEW
48. `apps/web/src/components/common/Input.tsx` - NEW
49. `apps/web/src/components/common/Select.tsx` - NEW
50. `apps/web/src/components/common/Table.tsx` - NEW
51. `apps/web/src/components/common/Modal.tsx` - NEW
52. `apps/web/src/components/common/Toast.tsx` - NEW
53. `apps/web/src/components/common/Loading.tsx` - NEW

**Layout (Phase 3):**

54. `apps/web/src/components/layout/Header.tsx` - NEW
55. `apps/web/src/components/layout/Sidebar.tsx` - NEW
56. `apps/web/src/components/layout/MainLayout.tsx` - NEW

**Auth (Phase 3):**

57. `apps/web/src/pages/LoginPage.tsx` - NEW
58. `apps/web/src/store/auth.ts` - MODIFY
59. `apps/web/src/router/index.tsx` - MODIFY

**Participants (Phase 3):**

60. `apps/web/src/pages/participants/ParticipantListPage.tsx` - NEW
61. `apps/web/src/pages/participants/ParticipantDetailPage.tsx` - NEW

**Groups (Phase 3):**

62. `apps/web/src/pages/groups/GroupListPage.tsx` - NEW
63. `apps/web/src/pages/groups/GroupDetailPage.tsx` - NEW

**Sessions (Phase 3):**

64. `apps/web/src/pages/sessions/SessionListPage.tsx` - NEW
65. `apps/web/src/pages/sessions/SessionDetailPage.tsx` - NEW
66. `apps/web/src/pages/sessions/PresenceRecordingPage.tsx` - NEW

**Presence Components (Phase 3):**

67. `apps/web/src/components/presence/ParticipantList.tsx` - NEW
68. `apps/web/src/components/presence/PresenceToggle.tsx` - NEW
69. `apps/web/src/components/presence/BulkMarkPresent.tsx` - NEW
70. `apps/web/src/components/presence/QuickAddParticipant.tsx` - NEW

**Import (Phase 3):**

71. `apps/web/src/components/import/CSVUploader.tsx` - NEW
72. `apps/web/src/components/import/ImportProgress.tsx` - NEW
73. `apps/web/src/components/import/ImportErrors.tsx` - NEW

**Offline (Phase 3):**

74. `apps/web/src/utils/offlineStorage.ts` - NEW
75. `apps/web/src/hooks/useOfflineSync.ts` - NEW
76. `apps/web/src/hooks/useOnlineStatus.ts` - NEW

**Admin (Phase 4-6):**

77. `apps/web/src/pages/admin/ConflictListPage.tsx` - NEW
78. `apps/web/src/pages/admin/SyncHistoryPage.tsx` - NEW
79. `apps/web/src/pages/admin/AuditLogPage.tsx` - NEW
80. `apps/web/src/pages/admin/NotificationRulesPage.tsx` - NEW
81. `apps/web/src/components/admin/ConflictResolver.tsx` - NEW
82. `apps/web/src/components/admin/SideBySideComparison.tsx` - NEW

**Reports (Phase 5):**

83. `apps/web/src/pages/reports/ReportListPage.tsx` - NEW
84. `apps/web/src/pages/reports/AttendanceReportPage.tsx` - NEW
85. `apps/web/src/components/reports/ReportFilters.tsx` - NEW

**Notifications (Phase 6):**

86. `apps/web/src/components/notifications/NotificationBell.tsx` - NEW
87. `apps/web/src/components/notifications/NotificationList.tsx` - NEW

**Optional - External Portal (Phase 3):**

88. `apps/web/src/pages/external/ExternalSubmitPage.tsx` - NEW (OPTIONAL)
89. `apps/web/src/pages/external/ExternalConfirmationPage.tsx` - NEW (OPTIONAL)
90. `apps/web/src/pages/external/ExternalDataPage.tsx` - NEW (OPTIONAL)

**Tests (Phase 7):**

91. `apps/web/src/components/**/*.test.tsx` - NEW (multiple files)
92. `apps/web/src/pages/**/*.test.tsx` - NEW (multiple files)
93. `apps/web/src/utils/*.test.ts` - NEW (multiple files)
94. `apps/web/src/hooks/*.test.ts` - NEW (multiple files)
95. `apps/web/tests/api/*.test.ts` - NEW (multiple files)
96. `apps/web/tests/e2e/*.spec.ts` - NEW (multiple files)

### Infrastructure Files (Phase 8):

97. `docker-compose.yml` - MODIFY (production version)
98. `infrastructure/docker/nginx.conf` - MODIFY
99. `.env.production` - NEW
100. `docs/deployment.md` - NEW
101. `docs/monitoring.md` - NEW
102. `docs/troubleshooting.md` - NEW

---

## Verification Steps

### 1. Database verification:

```bash
cd apps/api
python manage.py makemigrations
python manage.py migrate
python manage.py check
```

### 2. Create test data:

```bash
python manage.py shell
>>> from app.models import Organization, User
>>> org = Organization.objects.create(name="Test School", slug="test-school", domain="education")
>>> User.objects.create_user(email="admin@test.com", password="test123", role="administrator", organization=org)
```

### 3. Start development server:

```bash
python manage.py runserver
# Test at http://localhost:8000/api/auth/login/
```

### 4. Frontend verification:

```bash
cd apps/web
npm install
npm run dev
# Test at http://localhost:5173
```

---

## Dependencies

This plan follows the WBS dependency order:

- **Phase 1 (Foundation)** must be completed first
- **Phase 2 (Core CRUD)** depends on Phase 1
- **Phase 3 (Frontend UI)** can partially proceed in parallel with Phase 2
- **Phases 4-8** depend on earlier phases completing

---

## Notes

- Start with **Phase 1: Foundation** (Database + Auth + Multi-tenancy)
- Each phase should be tested before moving to the next
- Use the existing documentation in `docs/technical/` as reference
- Follow Django REST Framework conventions
- Use Zustand for frontend state management
- Implement offline storage with IndexedDB in Phase 3
- Session-based authentication (Django built-in) will be used

---

## Summary of Items Added/Updated

### Previously Missing Items Now Included:

**Phase 1 (Foundation):**

- ✅ Organization settings storage (JSON field)
- ✅ Organization user scoping implementation details
- ✅ External participant permission class
- ✅ Configurable session expiration
- ✅ Notes about already-implemented middleware and permissions

**Phase 2 (Core CRUD):**

- ✅ Domain service for domain configuration logic
- ✅ Organization model additional fields (domain_type, settings)
- ✅ Domain terminology mapping
- ✅ Additional admin endpoints for domain config

**Phase 3 (Frontend UI):**

- ✅ Connection status detection hook
- ✅ Detailed IndexedDB schema
- ✅ Manual data entry UI components (presence recording)
- ✅ Bulk import UI components
- ✅ External participant portal (marked as optional)

**Phase 4 (Offline Sync):**

- ✅ Side-by-side conflict comparison component
- ✅ SyncHistory model and tracking
- ✅ Sync retry mechanism
- ✅ Sync status indicators

**Phase 5 (Reporting):**

- ✅ Frontend report pages and components
- ✅ Report caching implementation details
- ✅ Report scheduling (with Celery note)

**Phase 6 (Notifications & Governance):**

- ✅ Frontend notification components
- ✅ Notification rules engine details
- ✅ User notification preferences
- ✅ Audit log export endpoint
- ✅ Audit log query filters
- ✅ Retention configuration model
- ✅ Dry-run mode for retention cleanup

**Phase 7 (Testing):**

- ✅ Detailed test file structure for backend
- ✅ Detailed test file structure for frontend
- ✅ E2E test scenarios
- ✅ pytest.ini configuration
- ✅ Performance testing files and tools

**Phase 8 (Deployment):**

- ✅ Production docker-compose.yml details
- ✅ SSL/HTTPS setup with Let's Encrypt
- ✅ Backup strategy with example script
- ✅ Environment variable management
- ✅ Deployment documentation files to create

### Key Improvements:

1. **Better file organization** - Each phase now lists all files to create with clear paths
2. **Code snippets** - Added for models, configurations, and key components
3. **Frontend components** - Detailed breakdown of UI components needed
4. **API endpoints** - Comprehensive list of all endpoints with methods
5. **Testing structure** - Clear organization of test files
6. **Deployment details** - Production configuration specifics
7. **Missing WBS items** - All 24 work packages now covered in detail
