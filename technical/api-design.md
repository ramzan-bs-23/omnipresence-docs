# API Design: Omnipresence

## Overview

This document defines the RESTful API for Omnipresence. All endpoints support
the [functional requirements](../project-specification.md#4-functional-specifications) from the project specification.

**Base URL:** `https://api.omnipresence.example.com`

**Content-Type:** `application/json`

**Authentication:** Bearer token (JWT) or session cookie

---

## Response Format

All responses follow this structure:

```json
{
  "data": {
    ...
  },
  "errors": null,
  "meta": {
    "page": 1,
    "per_page": 50,
    "total": 125
  }
}
```

---

## Authentication

### POST /api/auth/login/

Authenticate with email and password.

**Request:**

```json
{
  "email": "user@example.com",
  "password": "secure_password"
}
```

**Response (200):**

```json
{
  "data": {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "user": {
      "id": 123,
      "email": "user@example.com",
      "role": "administrator",
      "organization": {
        "id": 1,
        "name": "Example School"
      }
    }
  }
}
```

### POST /api/auth/logout/

Invalidate current session/token.

**Request:** `{}`

**Response (200):** `{ "data": { "success": true } }`

---

## Organizations

### GET /api/organizations/

Get current user's organization (single org per user).

**Response (200):**

```json
{
  "data": {
    "id": 1,
    "name": "Example School",
    "slug": "example-school",
    "domain_type": "education"
  }
}
```

---

## Users

### GET /api/users/

List users in organization (admin only).

**Query Params:** `page`, `per_page`, `role`, `search`

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "email": "admin@example.com",
      "role": "administrator",
      "is_active": true,
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "meta": {
    "total": 5
  }
}
```

### POST /api/users/

Create new user (admin only).

**Request:**

```json
{
  "email": "newuser@example.com",
  "password": "secure_password",
  "role": "frontline"
}
```

### GET /api/users/{id}/

Get user details.

### PUT /api/users/{id}/

Update user (admin only, or self for limited fields).

---

## Participants

### GET /api/participants/

List participants in organization.

**Query Params:**

- `page`, `per_page` — Pagination
- `group_id` — Filter by group
- `search` — Search by name or identifier
- `is_active` — Filter by active status

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "external_id": "STU001",
      "first_name": "John",
      "last_name": "Doe",
      "identifier": "2024-001",
      "is_active": true,
      "groups": [
        {
          "id": 1,
          "name": "Class 10-A"
        }
      ]
    }
  ],
  "meta": {
    "total": 150
  }
}
```

### POST /api/participants/

Create single participant.

**Request:**

```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "identifier": "2024-002",
  "group_ids": [
    1,
    2
  ]
}
```

### POST /api/participants/bulk/

Bulk import participants (CSV upload).

**Request:** `multipart/form-data` with `file` field (CSV)

**CSV Format:**

```csv
first_name,last_name,identifier,group_names
John,Doe,2024-001,"Class 10-A"
Jane,Smith,2024-002,"Class 10-A;Class 10-B"
```

**Response (200):**

```json
{
  "data": {
    "created": 45,
    "updated": 5,
    "errors": [
      {
        "row": 12,
        "error": "Duplicate identifier"
      }
    ]
  }
}
```

### GET /api/participants/{id}/

Get participant details.

### PUT /api/participants/{id}/

Update participant.

---

## Groups

### GET /api/groups/

List groups in organization.

**Query Params:** `page`, `per_page`, `group_type`, `parent_id`

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Class 10-A",
      "group_type": "class",
      "parent_id": null,
      "participant_count": 30,
      "is_active": true
    }
  ],
  "meta": {
    "total": 12
  }
}
```

### POST /api/groups/

Create new group.

**Request:**

```json
{
  "name": "Class 11-A",
  "group_type": "class",
  "parent_id": null
}
```

### GET /api/groups/{id}/

Get group details with participants.

### PUT /api/groups/{id}/

Update group.

### DELETE /api/groups/{id}/

Delete group (if no sessions exist).

---

## Sessions

### GET /api/sessions/

List sessions.

**Query Params:**

- `page`, `per_page`
- `group_id` — Filter by group
- `date_from`, `date_to` — Date range
- `status` — 'scheduled', 'in_progress', 'completed'

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "name": "Math Class - Week 1",
      "group_id": 1,
      "scheduled_start_at": "2024-01-15T09:00:00Z",
      "scheduled_end_at": "2024-01-15T10:00:00Z",
      "actual_start_at": "2024-01-15T09:02:00Z",
      "actual_end_at": null,
      "presence_stats": {
        "total": 30,
        "present": 27,
        "absent": 3
      }
    }
  ],
  "meta": {
    "total": 50
  }
}
```

### POST /api/sessions/

Create new session.

**Request:**

```json
{
  "name": "Math Class - Week 2",
  "group_id": 1,
  "scheduled_start_at": "2024-01-22T09:00:00Z",
  "scheduled_end_at": "2024-01-22T10:00:00Z"
}
```

### GET /api/sessions/{id}/

Get session details with all presence records.

### PUT /api/sessions/{id}/

Update session.

### PATCH /api/sessions/{id}/start/

Mark session as started.

### PATCH /api/sessions/{id}/end/

Mark session as ended.

---

## Presence

### GET /api/presence/

List presence records.

**Query Params:**

- `page`, `per_page`
- `session_id` — Filter by session
- `participant_id` — Filter by participant
- `state` — Filter by presence state

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "session_id": 1,
      "participant": {
        "id": 1,
        "name": "John Doe",
        "identifier": "2024-001"
      },
      "presence_state": {
        "code": "present",
        "label": "Present"
      },
      "recorded_at": "2024-01-15T09:05:00Z",
      "recorded_by": {
        "id": 10,
        "name": "Teacher Jane"
      }
    }
  ],
  "meta": {
    "total": 30
  }
}
```

### POST /api/presence/

Record presence for a participant in a session.

**Request (single):**

```json
{
  "session_id": 1,
  "participant_id": 1,
  "presence_state_code": "present"
}
```

**Request (bulk):**

```json
{
  "session_id": 1,
  "records": [
    {
      "participant_id": 1,
      "presence_state_code": "present"
    },
    {
      "participant_id": 2,
      "presence_state_code": "absent"
    },
    {
      "participant_id": 3,
      "presence_state_code": "late"
    }
  ]
}
```

### POST /api/presence/sync/

Sync offline presence records (batch operation).

**Request:**

```json
{
  "device_id": "tablet-001",
  "records": [
    {
      "session_id": 1,
      "participant_id": 1,
      "presence_state_code": "present",
      "recorded_at": "2024-01-15T09:05:00Z"
    }
  ]
}
```

**Response (200):**

```json
{
  "data": {
    "synced": 28,
    "conflicts": [
      {
        "session_id": 1,
        "participant_id": 5,
        "conflict_id": 123
      }
    ]
  }
}
```

### PUT /api/presence/{id}/

Update presence record (with audit logging).

---

## Reports

### GET /api/reports/attendance/

Generate attendance report.

**Query Params:**

- `group_id` — Required
- `date_from` — Required
- `date_to` — Required
- `format` — 'json', 'csv', 'pdf'

**Response (200):**

```json
{
  "data": {
    "group": {
      "id": 1,
      "name": "Class 10-A"
    },
    "period": {
      "from": "2024-01-01",
      "to": "2024-01-31"
    },
    "summary": {
      "total_sessions": 20,
      "total_participants": 30,
      "overall_attendance_rate": 0.92
    },
    "by_participant": [
      {
        "participant_id": 1,
        "participant_name": "John Doe",
        "present": 18,
        "absent": 2,
        "late": 0,
        "attendance_rate": 0.90
      }
    ]
  }
}
```

### GET /api/reports/absentees/

Get list of absentees for a session.

**Query Params:** `session_id` (required)

### GET /api/reports/export/{report_id}/

Download exported report (CSV/PDF).

---

## Admin (Administrator Only)

### GET /api/admin/audit-logs/

Get audit log entries.

**Query Params:** `page`, `per_page`, `table_name`, `record_id`, `date_from`, `date_to`

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "table_name": "presence_records",
      "record_id": 123,
      "action": "update",
      "changed_by": {
        "id": 10,
        "name": "Admin User"
      },
      "old_values": {
        "presence_state_code": "absent"
      },
      "new_values": {
        "presence_state_code": "present"
      },
      "changed_at": "2024-01-15T10:30:00Z",
      "source_device": "web-001"
    }
  ],
  "meta": {
    "total": 150
  }
}
```

### POST /api/admin/audit-logs/export/

Export audit logs (CSV).

### GET /api/admin/sync-conflicts/

Get unresolved sync conflicts.

**Response (200):**

```json
{
  "data": [
    {
      "id": 123,
      "session_id": 1,
      "participant": {
        "id": 5,
        "name": "Student Five"
      },
      "version_a": {
        "presence_state_code": "present",
        "recorded_at": "2024-01-15T09:00:00Z",
        "source": "tablet-001"
      },
      "version_b": {
        "presence_state_code": "absent",
        "recorded_at": "2024-01-15T09:05:00Z",
        "source": "mobile-app"
      }
    }
  ]
}
```

### POST /api/admin/sync-conflicts/{id}/resolve/

Resolve a sync conflict by choosing the authoritative version.

**Request:**

```json
{
  "chosen_version": "a"
}
```

### GET /api/admin/presence-states/

Get presence states for organization (with domain config).

### POST /api/admin/presence-states/

Create custom presence state.

**Request:**

```json
{
  "domain": "education",
  "code": "late_excused",
  "label": "Late (Excused)",
  "color": "#ffa500"
}
```

---

## Notifications

### GET /api/notifications/

Get current user's notifications.

**Query Params:** `page`, `per_page`, `is_read`

**Response (200):**

```json
{
  "data": [
    {
      "id": 1,
      "type": "absence",
      "title": "Student Absent",
      "message": "John Doe was marked absent for Math Class",
      "link": "/sessions/1",
      "is_read": false,
      "created_at": "2024-01-15T10:00:00Z"
    }
  ],
  "meta": {
    "total": 5,
    "unread_count": 3
  }
}
```

### PATCH /api/notifications/{id}/read/

Mark notification as read.

### PATCH /api/notifications/read-all/

Mark all notifications as read.

---

## Error Responses

All errors follow this format:

```json
{
  "data": null,
  "errors": [
    {
      "code": "VALIDATION_ERROR",
      "message": "Invalid input data",
      "details": {
        "field": "email",
        "reason": "Email already exists"
      }
    }
  ],
  "meta": null
}
```

**Common HTTP Status Codes:**

- `200` — Success
- `201` — Created
- `400` — Bad Request (validation error)
- `401` — Unauthorized (not authenticated)
- `403` — Forbidden (no permission)
- `404` — Not Found
- `409` — Conflict (duplicate, sync conflict)
- `422` — Unprocessable Entity
- `500` — Internal Server Error

---

## Pagination

All list endpoints support pagination:

| Param      | Default | Max |
|------------|---------|-----|
| `page`     | 1       | —   |
| `per_page` | 50      | 100 |

Response includes `meta` with pagination info.

---

## Rate Limiting

- 100 requests per minute per user
- 1000 requests per minute per organization
- Rate limit headers included in all responses

---

## API Documentation

Interactive OpenAPI documentation available at:

- **Swagger UI:** `https://api.omnipresence.example.com/api/docs/`
- **OpenAPI JSON:** `https://api.omnipresence.example.com/api/schema/`

---

## Summary

This API design provides:

- ✅ RESTful endpoints for all resources
- ✅ Bulk operations for data input
- ✅ Offline sync support with conflict handling
- ✅ Exportable reports (CSV, PDF)
- ✅ Comprehensive audit logging
- ✅ In-app notifications
- ✅ Domain-configurable presence states
- ✅ Multi-tenancy via organization context

All endpoints support the [functional requirements](../project-specification.md#4-functional-specifications) from the
project specification.
