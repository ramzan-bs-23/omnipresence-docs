# Tech Stack: Omnipresence

## Overview

This document defines the technology choices for Omnipresence. The focus is on **simple, proven, robust** technologies
that support all requirements from the [project specification](../project-specification.md).

---

## Technology Choices

| Layer                  | Technology             | Version | Why                                                      |
|------------------------|------------------------|---------|----------------------------------------------------------|
| **Backend API**        | Django REST Framework  | 5.0+    | Proven, batteries-included, excellent ORM, built-in auth |
| **Frontend UI**        | React + Vite           | 18+, 5+ | Fast build, standard ecosystem, no framework overhead    |
| **Database**           | MySQL                  | 8.0+    | Reliable, ACID compliant, widely supported               |
| **State Management**   | Zustand                | 4+      | Simple, lightweight, minimal boilerplate                 |
| **API Documentation**  | drf-spectacular        | 0.27+   | Auto-generated OpenAPI from Django                       |
| **Testing (Backend)**  | Pytest                 | 7.0+    | Standard Python testing, fixtures, coverage              |
| **Testing (Frontend)** | Vitest                 | 1.0+    | Fast unit tests, Vite-native                             |
| **Testing (E2E)**      | Playwright             | 1.40+   | Cross-browser E2E testing                                |
| **Deployment**         | Docker, Docker Compose | 24+     | Consistent environments, simple orchestration            |

---

## Backend: Django REST Framework

### Why Django REST?

- **Batteries included** — Auth, admin panel, ORM, migrations built-in
- **Mature ecosystem** — 15+ years of development, extensive libraries
- **ORM capabilities** — Powerful query interface, handles complex relationships
- **Multi-tenancy support** — Easy to implement via organization scoping
- **Admin interface** — Free CRUD interface for data management
- **Security** — Built-in CSRF protection, SQL injection prevention

### Key Packages

```python
# Backend dependencies (pyproject.toml)
[dependencies]
django = "^5.0"
djangorestframework = "^3.14"
drf - spectacular = "^0.27"
django - cors - headers = "^4.3"
mysqlclient = "^2.2"
django - extensions = "^3.2"
pytest - django = "^4.7"
```

---

## Frontend: React + Vite

### Why React + Vite (not Next.js)?

- **Simplicity** — No SSR complexity for this use case
- **Fast development** — Vite instant HMR, no build wait
- **Smaller bundle** — Client-only, no server-side overhead
- **Standard** — No framework-specific patterns to learn
- **SPA focus** — Presence tracking is an interactive application

### Key Packages

```json
{
  "dependencies": {
    "react": "^18.2",
    "react-dom": "^18.2",
    "react-router-dom": "^6.21",
    "zustand": "^4.4",
    "@tanstack/react-query": "^5.17"
  },
  "devDependencies": {
    "vite": "^5.0",
    "vitest": "^1.1",
    "@playwright/test": "^1.40"
  }
}
```

---

## State Management: Zustand

### Why Zustand over Redux Toolkit?

- **Simpler API** — No actions, reducers, dispatch
- **Less boilerplate** — Define store, use store
- **Smaller bundle** — ~1KB vs Redux Toolkit's ~10KB
- **TypeScript friendly** — Excellent inference
- **Sufficient for this app** — No complex state orchestration needed

### Example

```typescript
// Simple Zustand store
import {create} from 'zustand';

interface PresenceStore {
    isRecording: boolean;
    toggleRecording: () => void;
}

export const usePresenceStore = create<PresenceStore>((set) => ({
    isRecording: false,
    toggleRecording: () => set((state) => ({isRecording: !state.isRecording})),
}));
```

---

## Database: MySQL

### Why MySQL over PostgreSQL?

- **Proven reliability** — Decades of production use
- **Wide support** — Available everywhere, easy hosting
- **Simple replication** — Built-in master-slave replication
- **Good performance** — Excellent for read-heavy workloads
- **Familiar** — Most developers know MySQL

### Data Types

| Concept           | MySQL Type                            |
|-------------------|---------------------------------------|
| IDs               | `BIGINT UNSIGNED` (auto-increment)    |
| Foreign keys      | `BIGINT UNSIGNED` (indexed)           |
| Names/Identifiers | `VARCHAR(255)`                        |
| Timestamps        | `DATETIME(6)` (microsecond precision) |
| JSON data         | `JSON`                                |
| Boolean flags     | `BOOLEAN` (TINYINT(1))                |

---

## API Documentation: drf-spectacular

Auto-generates OpenAPI 3.0 schema from Django REST serializers and views.

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

INSTALLED_APPS = [
    'drf_spectacular',
]
```

Access at: `http://localhost:8000/api/schema/`

---

## Testing Stack

| Tool           | Purpose                            |
|----------------|------------------------------------|
| **Pytest**     | Backend unit and integration tests |
| **Vitest**     | Frontend unit tests (Vite-native)  |
| **Playwright** | End-to-end browser tests           |

### Coverage Goals

- Backend: 80%+ code coverage
- Frontend: 70%+ code coverage (components, services)
- E2E: Critical user paths (login, record presence, generate report)

---

## Deployment: Docker + Docker Compose

### Why Docker Compose (not Kubernetes)?

- **Simpler** — YAML config vs complex manifests
- **Sufficient** — Handles dev, staging, and single-server production
- **Local-first** — Same config runs locally and in production
- **Easy debugging** — Direct container access
- **Lower cost** — Can run on single VPS

### Services

```yaml
# docker-compose.yml
services:
  mysql:      # Database
  api:        # Django REST backend
  web:        # React + Vite frontend
  nginx:      # Reverse proxy (production only)
```

---

## Version Requirements

| Tool    | Minimum Version |
|---------|-----------------|
| Python  | 3.11+           |
| Node.js | 18+             |
| MySQL   | 8.0+            |
| Docker  | 24.0+           |

---

## Summary

This tech stack prioritizes:

1. **Simplicity** — Standard tools, minimal complexity
2. **Robustness** — Proven, battle-tested technologies
3. **Developer experience** — Fast iteration, good tooling
4. **Maintainability** — Large communities, long-term support

All choices support the requirements in the [project specification](../project-specification.md) without
over-engineering.
