# Omnipresence

A unified presence and attendance management platform for education, hospitality, events, and corporate environments.

## Overview

Omnipresence enables organizations to reliably mark, track, and understand "who was present, where, and when" with
minimal effort from users. The system works across multiple domains and supports offline operation.

## Tech Stack

| Layer                | Technology                                   |
|----------------------|----------------------------------------------|
| **Backend**          | Django REST Framework 5.0+ with Python 3.11+ |
| **Frontend**         | React 18+ with Vite 5+ and TypeScript        |
| **Database**         | MySQL 8.0+                                   |
| **State Management** | Zustand                                      |
| **Deployment**       | Docker + Docker Compose                      |

## Project Structure

```
omnipresence/
├── README.md                  # This file
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore patterns
├── docker-compose.yml         # Docker orchestration
│
├── docs/                      # Documentation
│   ├── project-concept.md     # Vision, problem statement, market analysis
│   ├── project-specification.md  # Functional and non-functional requirements
│   ├── wbs.md                 # Work Breakdown Structure (24 work packages)
│   └── technical/             # Technical documentation
│       ├── tech-stack.md      # Technology choices and rationale
│       ├── architecture.md    # System architecture and design patterns
│       ├── database-schema.md # Database tables and relationships
│       ├── api-design.md      # REST API endpoints
│       └── development-setup.md  # Development environment setup
│
├── apps/                      # Application code
│   ├── api/                   # Backend (Django REST)
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── settings.py     # Django settings
│   │   │   ├── urls.py         # Root URL configuration
│   │   │   ├── wsgi.py         # WSGI config
│   │   │   ├── asgi.py         # ASGI config
│   │   │   ├── models/         # Django models
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base.py      # Base models (User, TimeStampedModel)
│   │   │   │   └── organization.py
│   │   │   ├── api/            # API endpoints
│   │   │   │   ├── __init__.py
│   │   │   │   └── urls.py
│   │   │   ├── core/           # Core components (middleware, permissions)
│   │   │   │   └── __init__.py
│   │   │   ├── services/       # Business logic services
│   │   │   │   └── __init__.py
│   │   │   └── utils/          # Utilities
│   │   ├── tests/              # Backend tests
│   │   ├── manage.py           # Django management script
│   │   └── requirements.txt    # Python dependencies
│   │
│   └── web/                   # Frontend (React + Vite)
│       ├── public/
│       ├── src/
│       │   ├── main.tsx        # React entry point
│       │   ├── App.tsx         # Root app component
│       │   ├── components/     # React components
│       │   │   └── common/      # Common UI components
│       │   ├── pages/          # Page components
│       │   ├── api/            # API client
│       │   ├── store/          # Zustand stores
│       │   ├── types/          # TypeScript types
│       │   ├── hooks/          # Custom hooks
│       │   └── utils/          # Utilities
│       ├── index.html          # HTML entry point
│       ├── vite.config.ts      # Vite configuration
│       ├── tsconfig.json       # TypeScript config
│       └── package.json        # NPM dependencies
│
└── infrastructure/            # Deployment and DevOps
    └── docker/                 # Docker configurations
        ├── api.Dockerfile     # Backend container
        ├── web.Dockerfile     # Frontend container
        └── nginx.conf         # Nginx config (production)
```

## Quick Start

### Using Docker (Recommended)

```bash
# Start all services (MySQL, API, Web)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000/api/
- **Django Admin:** http://localhost:8000/admin/

### Using Makefile

```bash
# Start development servers (backend + frontend)
make dev

# Start backend only
make dev.backend

# Start frontend only
make dev.frontend

# Run tests
make test

# Docker commands
make docker.up
make docker.logs
make docker.down
```

### Manual Setup

#### Backend

```bash
cd apps/api

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Frontend

```bash
cd apps/web

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run development server
npm run dev
```

## Documentation

| Document                                                 | Description                                |
|----------------------------------------------------------|--------------------------------------------|
| [Project Concept](docs/project-concept.md)               | Vision, problem statement, market analysis |
| [Project Specification](docs/project-specification.md)   | Functional and non-functional requirements |
| [Work Breakdown Structure](docs/wbs.md)                  | Implementation plan with 24 work packages  |
| [Tech Stack](docs/technical/tech-stack.md)               | Technology choices and rationale           |
| [Architecture](docs/technical/architecture.md)           | System architecture and design patterns    |
| [Database Schema](docs/technical/database-schema.md)     | Database tables and relationships          |
| [API Design](docs/technical/api-design.md)               | REST API endpoints                         |
| [Development Setup](docs/technical/development-setup.md) | Development environment setup              |

## Development

### Backend Commands

```bash
cd apps/api

# Run tests
pytest

# Run tests with coverage
pytest --cov

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Check Django configuration
python manage.py check
```

### Frontend Commands

```bash
cd apps/web

# Run tests
npm run test

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- **Multi-domain support** - Education, hospitality, events, corporate
- **Configurable presence states** - Domain-specific states (present, absent, late, excused, etc.)
- **Offline-first operation** - Works without internet, syncs when connection restored
- **Sync conflict resolution** - Detects and resolves conflicts from offline data
- **Bulk data import** - CSV import for participants and groups
- **Report generation** - CSV and PDF export with customizable filters
- **Comprehensive audit logging** - Track all data changes with source attribution
- **In-app notifications** - Alerts for absences, conflicts, and data quality issues
- **Multi-tenancy** - Complete data isolation between organizations

## Status

🚧 **Under Development** - This is the project scaffold/structure. Implementation is planned according to
the [Work Breakdown Structure](docs/wbs.md).

## License

[Add your license here]
