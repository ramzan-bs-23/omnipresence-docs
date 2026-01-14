# Project Specification: Omnipresence

## 1. Purpose

This document defines the **functional** and **non-functional** specifications for **Omnipresence**, a unified platform for presence and attendance tracking across multiple domains.

The document describes **system capabilities and constraints**, without prescribing implementation details.

---

## 2. System Overview

### 2.1 Objective
Omnipresence aims to provide a single, adaptable system that enables organizations to record, manage, and analyze presence data with minimal effort from daily users.

### 2.2 Core Principles
- Simplicity for frontline users  
- Adaptability across domains  
- Reliability under limited connectivity  
- Reporting as a first-class capability  

---

## 3. User Roles

- **Frontline User**  
  Marks or validates presence data.

- **Administrator**  
  Configures groups, participants, and oversees data quality.

- **Manager / Viewer**  
  Accesses reports and summaries without modifying data.

- **External Participant (Optional)**
  Submits presence-related information through controlled access.

---

### 3.1 Data Concepts

The following core entities define the conceptual model of the system:

| Entity | Definition |
|--------|------------|
| **Participant** | An individual whose presence is tracked (e.g., student, guest, attendee) |
| **Group** | A logical collection of participants (e.g., class, room, session type) |
| **Session / Occurrence** | A specific time-bound event where presence is recorded |
| **Presence Record** | A record linking one participant to one session with a presence status |
| **Organization** | The boundary for data isolation and access control |
| **User** | A system actor with authentication credentials and assigned role(s) |

**Key Relationships:**
- An Organization contains Groups, Participants, Users, and Sessions
- A Participant belongs to one or more Groups
- A Session occurs within a Group context
- A Presence Record associates one Participant with one Session
- A User is scoped to a single Organization

---

## 4. Functional Specifications

### 4.1 Domain and Mode Support
- The system shall support multiple operational domains (e.g., education, hospitality, events).
- Domain behavior shall be configurable without altering core system logic.
- Domain selection shall influence terminology, grouping, and reporting context.

---

### 4.2 Group and Participant Management
- The system shall allow definition of logical groups (e.g., classes, rooms, sessions).
- Participants shall be assignable to one or more groups.
- The system shall support bulk and incremental participant entry.

---

### 4.3 Presence Recording
- The system shall allow recording of presence for participants within a group and time context.
- Presence records shall be associated with a specific session or occurrence.
- The system shall prevent unintended duplication of presence records.

#### 4.3.1 Presence States
- The system shall support a core set of presence states:
  - `present` — Participant was present
  - `absent` — Participant was not present
- The system shall allow domain-specific configuration of additional presence states (e.g., `late`, `excused`, `partial`, `checked_in`, `checked_out`).
- Presence states shall be configurable per domain without code changes.
- The system shall support at least 10 domain-defined presence states.

---

### 4.4 Data Input Flexibility
- The system shall support bulk data input using familiar tabular formats.
- The system shall allow on-the-spot data entry for unplanned participants.
- The system shall support self-service data submission where applicable.

---

### 4.5 Offline Operation
- The system shall support presence recording without continuous internet connectivity.
- Presence data captured offline shall be retained and synchronized when connectivity is available.
- When synchronization detects conflicting presence records for the same participant and session, the system shall:
  - Record both versions with source and timestamp
  - Flag the conflict for administrator review
  - Allow administrator to designate the authoritative version
- The system shall preserve all synchronization history for conflict resolution.
- The system shall prevent automatic overwriting of data during sync conflicts.

---

### 4.6 Reporting and Outputs
- The system shall provide operational presence summaries.
- The system shall support aggregated reports over configurable time ranges.
- Reports shall be exportable in CSV format.
- Reports shall be exportable in PDF format.
- Exported data shall include timestamps, participant identifiers, and presence status.
- Exported files shall be named descriptively including report type and date range.

---

### 4.7 Data Governance
- The system shall maintain traceability for presence data changes.
- The system shall support controlled updates to previously recorded data.
- The system shall log all changes to presence records including:
  - Who made the change (user identifier)
  - What was changed (previous and new values)
  - When the change occurred (timestamp)
  - The source of the change (device or system identifier)
- Audit logs shall be exportable by administrators.
- Audit logs shall be retained for at least 1 year.
- Audit logs shall be immutable (once written, cannot be modified).

---

### 4.8 Authentication and Multi-Tenancy
- The system shall support user authentication via email and password.
- The system shall enforce organizational data isolation (multi-tenancy).
- Users shall be scoped to a single organization.
- The system shall support the following user roles:
  - **Frontline User** — Can create and modify presence records
  - **Administrator** — Can manage groups, participants, users, and configuration
  - **Manager / Viewer** — Read-only access to reports
  - **External Participant** — Limited self-service access (optional)
- The system shall allow administrators to create and manage user accounts.
- The system shall support session expiration after configurable inactivity periods.

---

### 4.9 Notifications
- The system shall support configurable notifications for:
  - Absent participants (e.g., when a participant is marked absent)
  - Conflict alerts (e.g., when sync conflicts require resolution)
  - Data quality issues (e.g., missing or inconsistent participant information)
- Notifications shall be delivered within the system (in-app).
- Administrators shall be able to configure notification rules per domain.
- Users shall be able to manage their notification preferences.

---

## 5. Non-Functional Specifications

### 5.1 Usability
- The system shall be usable by non-technical users with minimal training.
- Core workflows shall minimize repetitive actions.

---

### 5.2 Reliability
- The system shall function under intermittent network conditions.
- Presence data shall not be lost due to temporary connectivity issues.

---

### 5.3 Performance
- The system shall support concurrent usage by multiple users.
- Performance shall remain acceptable for both small and large groups.
- Core presence recording operations shall complete within 3 seconds.
- Report generation shall complete within 10 seconds for standard time ranges (daily, weekly, monthly).
- The system shall support at least 50 concurrent users within an organization.
- The system shall support presence recording for groups of up to 500 participants.
- Offline data synchronization shall complete within 30 seconds when connectivity is restored.

---

### 5.4 Scalability
- The system shall scale from small organizations to large institutions.
- Scaling shall not require changes to user workflows.

---

### 5.5 Security
- The system shall enforce role-based access control.
- Data access shall be restricted based on organizational boundaries.

---

### 5.6 Maintainability
- Domain-specific behavior shall be configurable.
- The system shall support evolution without disrupting existing domains.

---

### 5.7 Portability
- The system shall be usable across common device types.
- No specialized hardware shall be required.

---

### 5.8 Data Retention
- Presence records shall be retained for a minimum of 3 years.
- Organizations shall be able to configure longer retention periods.
- Deleted organizations shall have their data anonymized or permanently deleted within 90 days.
- Audit logs shall be retained separately from presence records.

---

## 6. Scope Boundaries

### 6.1 In Scope
- Presence and attendance tracking  
- Multi-domain adaptability  
- Offline-capable data capture  
- Reporting and data export  

### 6.2 Out of Scope
- Payroll, billing, grading, or compliance systems  
- Predictive or AI-driven analytics  
- Hardware-based identification solutions  

---

## 7. Success Criteria

The system shall be considered successful if it:
- Reduces effort required to record presence  
- Improves consistency and reliability of presence data  
- Works across multiple domains without redesign  
- Produces usable reports without manual processing  

---

## 8. Conclusion

Omnipresence is specified as a **domain-agnostic presence infrastructure**, designed to balance simplicity, adaptability, and reliability.  
This specification establishes a clear boundary between **what the system must support** and **how it may be implemented**.
