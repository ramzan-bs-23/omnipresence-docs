/**
 * TypeScript type definitions matching the API response structure.
 */

export interface ApiResponse<T> {
  data: T
  errors: null | ApiError[]
  meta: ResponseMeta | null
}

export interface ApiError {
  code: string
  message: string
  details?: Record<string, unknown>
}

export interface ResponseMeta {
  page: number
  per_page: number
  total: number
}

// Domain types
export type UserRole = 'frontline' | 'administrator' | 'manager' | 'external'

export type DomainType = 'education' | 'hospitality' | 'events' | 'corporate'

// Entities
export interface Organization {
  id: number
  name: string
  slug: string
  domain_type: DomainType
  created_at: string
  updated_at: string
}

export interface User {
  id: number
  email: string
  role: UserRole
  is_active: boolean
  last_login_at: string | null
  created_at: string
  updated_at: string
  organization?: Organization
}

export interface Participant {
  id: number
  external_id: string | null
  first_name: string
  last_name: string
  identifier: string
  date_of_birth: string | null
  is_active: boolean
  created_at: string
  updated_at: string
  groups?: Group[]
}

export interface Group {
  id: number
  name: string
  group_type: string
  parent_id: number | null
  is_active: boolean
  participant_count?: number
  created_at: string
  updated_at: string
}

export interface Session {
  id: number
  name: string
  group_id: number
  scheduled_start_at: string
  scheduled_end_at: string
  actual_start_at: string | null
  actual_end_at: string | null
  presence_stats?: {
    total: number
    present: number
    absent: number
  }
  created_at: string
  updated_at: string
}

export interface PresenceRecord {
  id: number
  session_id: number
  participant: {
    id: number
    first_name: string
    last_name: string
    identifier: string
  }
  presence_state: {
    code: string
    label: string
    color: string
  }
  recorded_at: string
  recorded_by: {
    id: number
    email: string
  }
}

export interface Notification {
  id: number
  type: string
  title: string
  message: string
  link: string | null
  is_read: boolean
  created_at: string
}

// Auth types
export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  token: string
  user: User
}

export interface SyncRequest {
  device_id: string
  records: SyncRecord[]
}

export interface SyncRecord {
  session_id: number
  participant_id: number
  presence_state_code: string
  recorded_at: string
}

export interface SyncResponse {
  synced: number
  conflicts: SyncConflict[]
}

export interface SyncConflict {
  session_id: number
  participant_id: number
  conflict_id: number
}

// Report types
export interface AttendanceReport {
  group: {
    id: number
    name: string
  }
  period: {
    from: string
    to: string
  }
  summary: {
    total_sessions: number
    total_participants: number
    overall_attendance_rate: number
  }
  by_participant: ParticipantReport[]
}

export interface ParticipantReport {
  participant_id: number
  participant_name: string
  present: number
  absent: number
  late: number
  attendance_rate: number
}
