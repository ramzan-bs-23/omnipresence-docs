# Database Schema: Omnipresence

## Overview

This document defines the MySQL database schema for Omnipresence. The design supports
all [data concepts](../project-specification.md#31-data-concepts)
and [functional requirements](../project-specification.md#4-functional-specifications) from the project specification.

---

## Core Tables

### 1. organizations

Tenant isolation — every organization has separate data.

| Column      | Type            | Notes                                      |
|-------------|-----------------|--------------------------------------------|
| id          | BIGINT UNSIGNED | Primary key, auto-increment                |
| name        | VARCHAR(255)    | Organization name                          |
| slug        | VARCHAR(50)     | Unique identifier for URLs                 |
| domain_type | VARCHAR(50)     | 'education', 'hospitality', 'events', etc. |
| created_at  | DATETIME(6)     | Creation timestamp                         |
| updated_at  | DATETIME(6)     | Last update timestamp                      |

**Indexes:**

- UNIQUE on `slug`
- INDEX on `domain_type`

---

### 2. users

System users with authentication and roles.

| Column          | Type            | Notes                                               |
|-----------------|-----------------|-----------------------------------------------------|
| id              | BIGINT UNSIGNED | Primary key, auto-increment                         |
| organization_id | BIGINT UNSIGNED | Foreign key → organizations.id                      |
| email           | VARCHAR(255)    | Login email (unique within org)                     |
| password_hash   | VARCHAR(255)    | Bcrypt hash                                         |
| role            | VARCHAR(50)     | 'frontline', 'administrator', 'manager', 'external' |
| is_active       | BOOLEAN         | Account status                                      |
| last_login_at   | DATETIME(6)     | Last login timestamp                                |
| created_at      | DATETIME(6)     | Creation timestamp                                  |
| updated_at      | DATETIME(6)     | Last update timestamp                               |

**Indexes:**

- UNIQUE on `(organization_id, email)`
- INDEX on `organization_id`
- INDEX on `role`

---

### 3. participants

People whose presence is tracked (students, guests, attendees).

| Column          | Type            | Notes                                |
|-----------------|-----------------|--------------------------------------|
| id              | BIGINT UNSIGNED | Primary key, auto-increment          |
| organization_id | BIGINT UNSIGNED | Foreign key → organizations.id       |
| external_id     | VARCHAR(100)    | External system reference (optional) |
| first_name      | VARCHAR(100)    | First name                           |
| last_name       | VARCHAR(100)    | Last name                            |
| identifier      | VARCHAR(100)    | Student ID, badge number, etc.       |
| date_of_birth   | DATE            | Optional (for some domains)          |
| extra_data      | JSON            | Domain-specific additional data      |
| is_active       | BOOLEAN         | Active status                        |
| created_at      | DATETIME(6)     | Creation timestamp                   |
| updated_at      | DATETIME(6)     | Last update timestamp                |

**Indexes:**

- UNIQUE on `(organization_id, identifier)`
- INDEX on `organization_id`
- INDEX on `is_active`

---

### 4. groups

Logical collections (classes, rooms, session types).

| Column          | Type            | Notes                                 |
|-----------------|-----------------|---------------------------------------|
| id              | BIGINT UNSIGNED | Primary key, auto-increment           |
| organization_id | BIGINT UNSIGNED | Foreign key → organizations.id        |
| parent_id       | BIGINT UNSIGNED | Optional parent group (for hierarchy) |
| name            | VARCHAR(255)    | Group name                            |
| group_type      | VARCHAR(50)     | 'class', 'room', 'session_type', etc. |
| extra_data      | JSON            | Domain-specific configuration         |
| is_active       | BOOLEAN         | Active status                         |
| created_at      | DATETIME(6)     | Creation timestamp                    |
| updated_at      | DATETIME(6)     | Last update timestamp                 |

**Indexes:**

- INDEX on `organization_id`
- INDEX on `parent_id`
- INDEX on `group_type`
- INDEX on `is_active`

---

### 5. group_memberships

Many-to-many relationship between participants and groups.

| Column         | Type            | Notes                         |
|----------------|-----------------|-------------------------------|
| id             | BIGINT UNSIGNED | Primary key, auto-increment   |
| group_id       | BIGINT UNSIGNED | Foreign key → groups.id       |
| participant_id | BIGINT UNSIGNED | Foreign key → participants.id |
| joined_at      | DATETIME(6)     | When participant joined group |
| extra_data     | JSON            | Role or section within group  |

**Indexes:**

- UNIQUE on `(group_id, participant_id)`
- INDEX on `group_id`
- INDEX on `participant_id`

---

### 6. sessions

Time-bound events where presence is recorded.

| Column             | Type            | Notes                          |
|--------------------|-----------------|--------------------------------|
| id                 | BIGINT UNSIGNED | Primary key, auto-increment    |
| organization_id    | BIGINT UNSIGNED | Foreign key → organizations.id |
| group_id           | BIGINT UNSIGNED | Foreign key → groups.id        |
| name               | VARCHAR(255)    | Session name                   |
| scheduled_start_at | DATETIME(6)     | Scheduled start time           |
| scheduled_end_at   | DATETIME(6)     | Scheduled end time             |
| actual_start_at    | DATETIME(6)     | Actual start time (nullable)   |
| actual_end_at      | DATETIME(6)     | Actual end time (nullable)     |
| extra_data         | JSON            | Domain-specific session data   |
| created_at         | DATETIME(6)     | Creation timestamp             |
| updated_at         | DATETIME(6)     | Last update timestamp          |

**Indexes:**

- INDEX on `organization_id`
- INDEX on `group_id`
- INDEX on `scheduled_start_at`

---

### 7. presence_records

Attendance records linking participants to sessions with status.

| Column            | Type            | Notes                                 |
|-------------------|-----------------|---------------------------------------|
| id                | BIGINT UNSIGNED | Primary key, auto-increment           |
| organization_id   | BIGINT UNSIGNED | Foreign key → organizations.id        |
| session_id        | BIGINT UNSIGNED | Foreign key → sessions.id             |
| participant_id    | BIGINT UNSIGNED | Foreign key → participants.id         |
| presence_state_id | BIGINT UNSIGNED | Foreign key → presence_states.id      |
| recorded_at       | DATETIME(6)     | When presence was recorded            |
| recorded_by       | BIGINT UNSIGNED | Foreign key → users.id (who recorded) |
| source_device_id  | VARCHAR(100)    | Device identifier for sync conflicts  |
| extra_data        | JSON            | Additional notes or metadata          |
| created_at        | DATETIME(6)     | Creation timestamp                    |
| updated_at        | DATETIME(6)     | Last update timestamp                 |

**Indexes:**

- UNIQUE on `(session_id, participant_id)` (one record per participant per session)
- INDEX on `organization_id`
- INDEX on `session_id`
- INDEX on `participant_id`
- INDEX on `recorded_at`

---

### 8. presence_states

Configurable presence states per domain (present, absent, late, etc.).

| Column          | Type            | Notes                                    |
|-----------------|-----------------|------------------------------------------|
| id              | BIGINT UNSIGNED | Primary key, auto-increment              |
| organization_id | BIGINT UNSIGNED | Foreign key → organizations.id           |
| domain          | VARCHAR(50)     | 'education', 'hospitality', etc.         |
| code            | VARCHAR(50)     | State code ('present', 'absent', 'late') |
| label           | VARCHAR(100)    | Display label                            |
| color           | VARCHAR(7)      | Hex color for UI                         |
| sort_order      | INTEGER         | Display order                            |
| is_default      | BOOLEAN         | Whether this is a default state          |
| created_at      | DATETIME(6)     | Creation timestamp                       |
| updated_at      | DATETIME(6)     | Last update timestamp                    |

**Indexes:**

- UNIQUE on `(organization_id, domain, code)`
- INDEX on `organization_id`
- INDEX on `domain`

---

### 9. audit_logs

Immutable audit trail for all data changes (per [spec 4.7](../project-specification.md#47-data-governance)).

| Column          | Type            | Notes                          |
|-----------------|-----------------|--------------------------------|
| id              | BIGINT UNSIGNED | Primary key, auto-increment    |
| organization_id | BIGINT UNSIGNED | Foreign key → organizations.id |
| table_name      | VARCHAR(100)    | Table that was changed         |
| record_id       | BIGINT UNSIGNED | ID of the affected record      |
| action          | VARCHAR(20)     | 'create', 'update', 'delete'   |
| changed_by      | BIGINT UNSIGNED | Foreign key → users.id         |
| old_values      | JSON            | Previous values (for updates)  |
| new_values      | JSON            | New values                     |
| changed_at      | DATETIME(6)     | When change occurred           |
| source_device   | VARCHAR(100)    | Device identifier              |

**Indexes:**

- INDEX on `organization_id`
- INDEX on `(table_name, record_id)`
- INDEX on `changed_by`
- INDEX on `changed_at`

**Retention:** Minimum 1 year (per [spec 5.8](../project-specification.md#58-data-retention))

---

### 10. sync_conflicts

Stores conflicting versions from offline sync (per [spec 4.5](../project-specification.md#45-offline-operation)).

| Column           | Type            | Notes                              |
|------------------|-----------------|------------------------------------|
| id               | BIGINT UNSIGNED | Primary key, auto-increment        |
| organization_id  | BIGINT UNSIGNED | Foreign key → organizations.id     |
| session_id       | BIGINT UNSIGNED | Foreign key → sessions.id          |
| participant_id   | BIGINT UNSIGNED | Foreign key → participants.id      |
| version_a_data   | JSON            | First version with metadata        |
| version_b_data   | JSON            | Second version with metadata       |
| resolved_with_id | BIGINT UNSIGNED | ID of chosen resolution (nullable) |
| resolved_at      | DATETIME(6)     | Resolution timestamp (nullable)    |
| resolved_by      | BIGINT UNSIGNED | Foreign key → users.id (nullable)  |
| created_at       | DATETIME(6)     | When conflict was detected         |

**Indexes:**

- INDEX on `organization_id`
- INDEX on `session_id`
- INDEX on `participant_id`
- INDEX on `resolved_with_id` (nullable)

---

### 11. notifications

In-app notification queue (per [spec 4.9](../project-specification.md#49-notifications)).

| Column            | Type            | Notes                                 |
|-------------------|-----------------|---------------------------------------|
| id                | BIGINT UNSIGNED | Primary key, auto-increment           |
| organization_id   | BIGINT UNSIGNED | Foreign key → organizations.id        |
| user_id           | BIGINT UNSIGNED | Foreign key → users.id (recipient)    |
| notification_type | VARCHAR(50)     | 'absence', 'conflict', 'data_quality' |
| title             | VARCHAR(255)    | Notification title                    |
| message           | TEXT            | Notification message                  |
| link              | VARCHAR(500)    | Optional link to related resource     |
| is_read           | BOOLEAN         | Read status                           |
| read_at           | DATETIME(6)     | When marked as read                   |
| created_at        | DATETIME(6)     | When notification was created         |

**Indexes:**

- INDEX on `organization_id`
- INDEX on `user_id`
- INDEX on `is_read`
- INDEX on `created_at`

---

## Entity Relationships

```
organizations (1) ──< (N) users
organizations (1) ──< (N) participants
organizations (1) ──< (N) groups
organizations (1) ──< (N) sessions
organizations (1) ──< (N) presence_records
organizations (1) ──< (N) presence_states
organizations (1) ──< (N) audit_logs
organizations (1) ──< (N) sync_conflicts
organizations (1) ──< (N) notifications

groups (1) ──< (N) sessions
groups (N) ──< (M) participants (via group_memberships)

sessions (1) ──< (N) presence_records
participants (1) ──< (N) presence_records
presence_states (1) ──< (N) presence_records
users (1) ──< (N) presence_records (recorded_by)
```

---

## Data Retention

Per [specification section 5.8](../project-specification.md#58-data-retention):

| Data Type             | Retention Period                     |
|-----------------------|--------------------------------------|
| Presence records      | Minimum 3 years (configurable)       |
| Audit logs            | Minimum 1 year, separate storage     |
| Deleted organizations | Anonymized or deleted within 90 days |

---

## Migration Strategy

- Django migrations manage schema changes
- All migrations are reversible
- Breaking changes require data migration scripts
- Backups required before destructive migrations

---

## Summary

This schema supports:

- ✅ All [data concepts](../project-specification.md#31-data-concepts)
- ✅ Multi-tenancy via `organization_id`
- ✅ Domain-configurable presence states
- ✅ Offline sync with conflict tracking
- ✅ Comprehensive audit logging
- ✅ In-app notifications
- ✅ Data retention policies

The design is **normalized, indexed, and production-ready** while remaining simple and maintainable.
