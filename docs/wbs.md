# Work Breakdown Structure (WBS): Omnipresence

**For AI Agent Implementation** - Simple, actionable tasks based on project-specification.md

---

## Phase 1: Foundation (Weeks 1-2)

### WP-001: Database Schema & Models

**Deliverable:** All database tables with relationships

- Create Organization model (name, slug, domain, settings)
- Create User model (email, password, role, organization_id)
- Create Participant model (identifier, name, metadata, organization_id)
- Create Group model (name, type, domain_config, organization_id)
- Create GroupMembership model (participant_id, group_id)
- Create Session model (schedule, location, group_id, organization_id)
- Create PresenceState model (name, is_core, domain_config, organization_id)
- Create PresenceRecord model (participant_id, session_id, state_id, recorded_by)
- Create AuditLog model (entity_type, entity_id, changes, user_id, timestamp, source)
- Create SyncConflict model (entity_id, server_version, client_version, resolved)
- Create Notification model (type, recipient_id, message, read_at)

### WP-002: Authentication & Authorization

**Deliverable:** Working login system with role-based access

- Implement email/password authentication
- Create user roles: frontline, administrator, manager, external
- Implement session management with configurable expiration
- Create role-based access control middleware
- Set up organization-scoped data queries

### WP-003: Multi-Tenancy Foundation

**Deliverable:** Organization data isolation working

- Implement organization middleware (set request.organization)
- Add organization_id filtering to all queries
- Create organization settings storage
- Implement organization user scoping (users see only their org data)

---

## Phase 2: Core Features (Weeks 3-4)

### WP-004: Participant & Group Management

**Deliverable:** CRUD operations for participants and groups

- Participant API: list, create, update, delete
- Group API: list, create, update, delete
- Group membership management (add/remove participants)
- Bulk participant import endpoint (CSV)
- Participant and group search/filter

### WP-005: Session Management

**Deliverable:** Session CRUD and scheduling

- Session API: list, create, update, delete
- Session scheduling (date, time, location)
- Session list with filtering by group/date range
- Session detail view with participants

### WP-006: Presence Recording

**Deliverable:** Record and update presence

- Presence record creation endpoint
- Bulk presence update (mark multiple participants)
- Duplicate prevention (one record per participant per session)
- Presence history retrieval
- Presence state validation

### WP-007: Domain Configuration

**Deliverable:** Per-domain customization

- Domain settings storage (education, hospitality, events, corporate)
- Domain-specific presence state configuration
- Domain terminology mapping (e.g., "student" vs "guest")
- Domain-driven UI hints

---

## Phase 3: Data Input (Weeks 5-6)

### WP-008: Manual Data Entry UI

**Deliverable:** Web interface for recording presence

- Session detail page with participant list
- Quick toggle buttons (present/absent/states)
- Bulk "mark all present" action
- On-the-spot participant creation
- Form validation and error handling

### WP-009: Bulk Data Import

**Deliverable:** CSV import system

- CSV file upload endpoint
- CSV parsing and validation
- Error reporting for invalid rows
- Import progress tracking
- Support for participants and groups import

### WP-010: Offline Data Capture

**Deliverable:** Frontend offline storage

- IndexedDB schema for local data
- Save presence records locally when offline
- Queue for pending sync
- Connection status detection
- Auto-sync when connection restored

### WP-011: External Participant Portal

**Deliverable:** Self-service interface (optional)

- Secure access for external participants
- Presence submission form
- Confirmation display
- Limited read-only access to own data

---

## Phase 4: Offline Sync (Weeks 7-8)

### WP-012: Sync Conflict Detection

**Deliverable:** Backend sync conflict handling

- Sync endpoint to receive offline data batches
- Compare client vs server records
- Detect conflicting data for same participant+session
- Create SyncConflict records when differences found
- Return sync results with conflict list

### WP-013: Sync Conflict Resolution

**Deliverable:** UI for resolving conflicts

- Conflict list view for administrators
- Side-by-side comparison of versions
- Manual resolution interface (choose server or client version)
- Resolution audit logging
- Bulk resolution actions

### WP-014: Sync History Management

**Deliverable:** Track all sync operations

- Store sync batch history
- Track device IDs and sync timestamps
- Sync status indicators
- Retry mechanism for failed syncs

---

## Phase 5: Reporting (Weeks 9-10)

### WP-015: Report Generation

**Deliverable:** Core reporting engine

- Operational summaries (daily, by session)
- Aggregate reports (weekly, monthly, custom ranges)
- Report filters: group, date range, presence state
- Report caching for performance
- Report scheduling (optional)

### WP-016: CSV Export

**Deliverable:** CSV export functionality

- Export presence records to CSV
- Include headers: timestamp, participant, session, status
- Descriptive file naming (report_type_date_range.csv)
- Export progress indicator for large datasets

### WP-017: PDF Export

**Deliverable:** PDF report generation

- PDF template design
- Include tables and summaries
- Descriptive file naming (report_type_date_range.pdf)
- Export progress indicator

---

## Phase 6: Notifications & Governance (Weeks 11-12)

### WP-018: Notification System

**Deliverable:** In-app notifications

- Notification creation API
- Notification list endpoint
- Mark as read/unread
- Notification rules engine (absent participants, conflicts)
- User notification preferences

### WP-019: Audit Logging

**Deliverable:** Complete audit trail

- Automatic logging of all presence record changes
- Log: who, what, when, previous value, new value, source
- Audit log query endpoint (with filters)
- Audit log export (CSV)
- Immutable log storage (no updates/deletes)

### WP-020: Data Retention

**Deliverable:** Automated cleanup

- Presence record retention (3 years minimum, configurable)
- Audit log retention (1 year)
- Soft delete for organizations (90-day anonymization)
- Retention configuration per organization

---

## Phase 7: Testing & Polish (Weeks 13-14)

### WP-021: Backend Testing

**Deliverable:** Test coverage for backend

- Unit tests for models and services
- API endpoint tests
- Multi-tenancy isolation tests
- Sync conflict scenario tests

### WP-022: Frontend Testing

**Deliverable:** Test coverage for frontend

- Component tests
- Integration tests (API calls)
- Offline sync simulation tests
- E2E tests for key workflows

### WP-023: Performance Testing

**Deliverable:** Performance targets met

- Test with 50+ concurrent users
- Test with 500+ participant groups
- Verify presence recording < 3 seconds
- Verify report generation < 10 seconds
- Verify sync completes < 30 seconds

---

## Phase 8: Deployment (Week 15)

### WP-024: Production Setup

**Deliverable:** Production-ready deployment

- Production database configuration
- Docker production images
- SSL/HTTPS setup
- Backup strategy
- Environment variable management
- Deployment documentation

---

## Dependencies

```
WP-001 (Database)
    ↓
WP-002 (Auth) → WP-003 (Multi-tenancy)
    ↓              ↓
WP-004 (Participants/Groups) → WP-005 (Sessions) → WP-006 (Presence Recording)
                                                    ↓
WP-007 (Domain Config)           WP-008 (Manual Entry) → WP-010 (Offline Storage)
                                  ↓                      ↓
                              WP-009 (Bulk Import)   WP-011 (Sync Conflict)
                                                              ↓
                                                         WP-012 (Resolution)
                                                              ↓
                                                    WP-015 (Reports) → WP-016 (CSV) → WP-017 (PDF)
                                                              ↓
                                                    WP-018 (Notifications)
                                                              ↓
                                                    WP-019 (Audit Log) → WP-020 (Retention)
                                                              ↓
                                                    WP-021-023 (Testing)
                                                              ↓
                                                    WP-024 (Deployment)
```

---

## Summary Table

| WP  | Name                  | Backend | Frontend | Days | Dep          |
|-----|-----------------------|---------|----------|------|--------------|
| 001 | Database Schema       | ✓       | -        | 3    | -            |
| 002 | Authentication        | ✓       | ✓        | 3    | 001          |
| 003 | Multi-Tenancy         | ✓       | -        | 2    | 002          |
| 004 | Participants & Groups | ✓       | ✓        | 4    | 003          |
| 005 | Sessions              | ✓       | ✓        | 3    | 004          |
| 006 | Presence Recording    | ✓       | ✓        | 4    | 005          |
| 007 | Domain Config         | ✓       | ✓        | 2    | 003          |
| 008 | Manual Entry UI       | -       | ✓        | 4    | 006          |
| 009 | Bulk Import           | ✓       | ✓        | 3    | 004          |
| 010 | Offline Storage       | -       | ✓        | 4    | 006          |
| 011 | External Portal       | ✓       | ✓        | 3    | 002,006      |
| 012 | Sync Conflict         | ✓       | -        | 3    | 010          |
| 013 | Conflict Resolution   | ✓       | ✓        | 3    | 012          |
| 014 | Sync History          | ✓       | ✓        | 2    | 012          |
| 015 | Reports               | ✓       | ✓        | 4    | 006          |
| 016 | CSV Export            | ✓       | ✓        | 2    | 015          |
| 017 | PDF Export            | ✓       | ✓        | 2    | 015          |
| 018 | Notifications         | ✓       | ✓        | 3    | 002          |
| 019 | Audit Logging         | ✓       | -        | 3    | 001          |
| 020 | Data Retention        | ✓       | -        | 2    | 019          |
| 021 | Backend Tests         | ✓       | -        | 3    | All core     |
| 022 | Frontend Tests        | -       | ✓        | 3    | All UI       |
| 023 | Performance           | ✓       | ✓        | 3    | All features |
| 024 | Deployment            | ✓       | ✓        | 3    | All          |

**Total: ~75 working days (~15 weeks with 1 AI agent, ~4 weeks with 4 parallel agents)**
