# Architecture: Omnipresence

## Overview

Omnipresence uses a **simple three-layer architecture**. This document describes the system design, key patterns, and
how all requirements from the [project specification](../project-specification.md) are supported.

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      PRESENTATION LAYER                     │
│                                                             │
│                    React + Vite Frontend                    │
│            Components + Zustand Store + API Client          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │  Components  │  │   Pages      │  │    Store     │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTP/REST (JSON)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                        │
│                                                             │
│                 Django REST Framework                       │
│              (Views + Services + Models)                    │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Views     │  │  Services    │  │   Models     │       │
│  │ (endpoints)  │  │ (business    │  │  (Django     │       │
│  │              │  │   logic)     │  │    ORM)      │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Django ORM
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                            │
│                                                             │
│                        MySQL 8.0                            │
│                                                             │
│  organizations  │  users  │  participants  │  groups        │
│  sessions       │  presence_records  │  audit_logs          │
│  sync_conflicts │  notifications  │  presence_states        │
└─────────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### 1. Presentation Layer (Frontend)

**Responsibilities:**

- UI rendering and user interaction
- State management (Zustand)
- API communication
- Offline data caching (for sync)

**Key Technologies:**

- React 18+ (components)
- React Router 6+ (navigation)
- Zustand (state management)
- TanStack Query (API caching)
- Vite (build tool)

---

### 2. Application Layer (Backend)

**Responsibilities:**

- HTTP request handling (Views)
- Business logic (Services)
- Data validation (Serializers)
- Authentication and authorization
- Multi-tenancy isolation

**Key Technologies:**

- Django 5+ (web framework)
- Django REST Framework 3+ (API)
- drf-spectacular (OpenAPI docs)

---

### 3. Data Layer (Database)

**Responsibilities:**

- Persistent storage
- Data integrity (foreign keys, constraints)
- Query optimization (indexes)
- Transaction management

**Key Technologies:**

- MySQL 8.0+ (relational database)
- Django ORM (query interface)

---

## Key Architectural Patterns

### Multi-Tenancy via Organization Scoping

Every table includes `organization_id` to ensure data isolation.

```python
# Base model with organization scoping
class TimeStampedModel(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
```

All queries automatically filter by `organization_id` via middleware.

---

### Service Layer Pattern

Keep views thin — business logic lives in services.

```python
# Example: PresenceService
class PresenceService:
    def record_presence(self, session_id, participant_id, status, user):
# Validate
# Check for duplicates
# Create record
# Log audit trail
# Return result
```

**Views handle:** HTTP, serialization, authentication
**Services handle:** Business rules, validation, side effects

---

### Repository Pattern via Django ORM

Use Django QuerySets as repositories — no custom abstraction needed.

```python
# Simple, effective repository pattern
class ParticipantQuerySet(models.QuerySet):
    def in_group(self, group_id):
        return self.filter(group_memberships__group_id=group_id)

    def active(self):
        return self.filter(is_active=True)
```

---

## Performance Targets

From [specification section 5.3](../project-specification.md#53-performance):

| Metric             | Target           | How                                  |
|--------------------|------------------|--------------------------------------|
| Presence recording | < 3 seconds      | Optimized queries, bulk operations   |
| Report generation  | < 10 seconds     | Database indexes, materialized views |
| Concurrent users   | 50+ per org      | Connection pooling, caching          |
| Group size         | 500 participants | Pagination, lazy loading             |
| Offline sync       | < 30 seconds     | Batch operations, conflict queuing   |

---

## Offline Sync Architecture

### Client-Side (Frontend)

```
1. User records presence offline
2. Stored in IndexedDB (browser storage)
3. Sync queue maintains order
4. On reconnect: batch POST to /api/sync/
```

### Server-Side (Backend)

```
1. Receive sync batch with client timestamps
2. Check for conflicts (same participant+session, different data)
3. If conflict: store both versions, flag for admin
4. If no conflict: apply changes
5. Return sync result with any conflicts
```

### Conflict Resolution

Per [specification section 4.5](../project-specification.md#45-offline-operation):

- Both versions stored in `sync_conflicts` table
- Admin reviews via `/api/admin/sync-conflicts/`
- Admin chooses authoritative version
- No automatic overwriting

---

## Domain Configuration

### How Domains Work

Per [specification section 4.1](../project-specification.md#41-domain-and-mode-support):

Domains are **configuration**, not code:

```python
# Presence states are configurable per domain
class PresenceState(TimeStampedModel):
    organization = models.ForeignKey(Organization)
    domain = models.CharField(max_length=50)  # 'education', 'hospitality', etc.
    code = models.CharField(max_length=50)  # 'present', 'absent', 'late'
    label = models.CharField(max_length=100)  # Display label
    color = models.CharField(max_length=7)  # '#00ff00'
    sort_order = models.IntegerField(default=0)
```

Domain selection changes:

- Terminology (labels)
- Available presence states
- Default group structure
- Report templates

---

## Security Architecture

### Authentication Flow

```
1. POST /api/auth/login/ with email+password
2. Server validates credentials
3. Returns JWT token (or session key)
4. Client includes token in Authorization header
5. Server validates token on each request
6. Token expires after configurable inactivity period
```

### Authorization

- Role-based access control (RBAC)
- Roles: Frontline User, Administrator, Manager/Viewer, External Participant
- Permissions checked at view level via Django decorators

### Data Isolation

- `organization_id` on all tables
- Query middleware filters by user's organization
- Users cannot access other organizations' data

---

## Data Flow Examples

### Recording Presence (Online)

```
User → Frontend → API Client
                ↓
        POST /api/presence/
                ↓
        View validates request
                ↓
        Service checks business rules
                ↓
        Model creates record
                ↓
        Audit log entry created
                ↓
        Response to frontend
                ↓
        UI updates via Zustand
```

### Recording Presence (Offline)

```
User → Frontend → IndexedDB (stored locally)
                ↓
        [Offline...]
                ↓
        Connectivity restored
                ↓
        POST /api/sync/ (batch)
                ↓
        Server processes batch
                ↓
        Conflicts flagged if needed
                ↓
        Response with sync results
                ↓
        Frontend updates local state
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────┐
│              Nginx (Optional)               │
│         Reverse Proxy + SSL                 │
└─────────────────────────────────────────────┘
                    │
    ┌───────────────┴───────────────┐
    ▼                               ▼
┌────────────────┐        ┌────────────────┐
│  Web Container │        │  API Container │
│  React+Vite    │        │  Django REST   │
│  (nginx serve) │        │  (gunicorn)    │
└────────────────┘        └────────────────┘
                                     │
                                     ▼
                          ┌────────────────┐
                          │  MySQL         │
                          │  (Database)    │
                          └────────────────┘
```

For development: `docker-compose up` runs all services locally.

---

## Summary

This architecture provides:

- **Simplicity** — Three clear layers, standard patterns
- **Robustness** — Proven technologies, minimal custom code
- **Flexibility** — Domain configuration without code changes
- **Offline support** — Client-side storage + sync conflict resolution
- **Multi-tenancy** — Organization-based data isolation

All requirements from the [project specification](../project-specification.md) are supported by this design.
