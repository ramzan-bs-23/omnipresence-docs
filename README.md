# Omnipresence

A unified presence and attendance management platform for education, hospitality, events, and corporate environments.

## Overview

Omnipresence enables organizations to reliably mark, track, and understand "who was present, where, and when" with
minimal effort from users. The system works across multiple domains and supports offline operation.

## Tech Stack

- **Backend:** Django REST Framework 5.0+ with Python 3.11+
- **Frontend:** React 18+ with Vite 5+ and TypeScript
- **Database:** MySQL 8.0+
- **State Management:** Zustand
- **Deployment:** Docker + Docker Compose

## Project Structure

```
omnipresence/
├── apps/
│   ├── api/              # Backend (Django REST)
│   └── web/              # Frontend (React + Vite)
├── infrastructure/
│   └── docker/           # Docker configurations
├── docker-compose.yml
├── .env.example
└── README.md
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

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000/api/
- API Docs: http://localhost:8000/api/docs/
- Django Admin: http://localhost:8000/admin/

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

- [Project Concept](project-concept.md) — Vision, problem statement, market analysis
- [Project Specification](project-specification.md) — Functional and non-functional requirements
- [Technical Documentation](technical/) — Architecture, API design, database schema, development setup

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
```

### Frontend Commands

```bash
cd apps/web

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Build for production
npm run build

# Preview production build
npm run preview
```

## Features

- Multi-domain support (education, hospitality, events, corporate)
- Configurable presence states per domain
- Offline-first operation with sync conflict resolution
- Bulk data import (CSV)
- Report generation (CSV, PDF export)
- Comprehensive audit logging
- In-app notifications
- Multi-tenancy with data isolation

## License

[Add your license here]
