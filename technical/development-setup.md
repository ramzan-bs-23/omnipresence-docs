# Development Setup: Omnipresence

## Overview

This guide explains how to set up a local development environment for Omnipresence.

---

## Prerequisites

| Tool    | Minimum Version | Install                                 |
|---------|-----------------|-----------------------------------------|
| Python  | 3.11+           | [python.org](https://www.python.org/)   |
| Node.js | 18+             | [nodejs.org](https://nodejs.org/)       |
| MySQL   | 8.0+            | [dev.mysql.com](https://dev.mysql.com/) |
| Docker  | 24.0+           | [docker.com](https://www.docker.com/)   |
| Git     | Latest          | [git-scm.com](https://git-scm.com/)     |

---

## Quick Start (Docker)

The fastest way to get started — uses Docker Compose for all services.

```bash
# Clone repository
git clone https://github.com/example/omnipresence.git
cd omnipresence

# Start services (MySQL, Redis)
docker-compose up -d

# Run backend
cd apps/api
poetry install
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Run frontend (new terminal)
cd apps/web
npm install
npm run dev
```

Visit `http://localhost:5173` for the frontend or `http://localhost:8000/api/docs/` for API docs.

---

## Manual Setup

If you prefer not to use Docker for MySQL:

### 1. Install MySQL

```bash
# macOS
brew install mysql
brew services start mysql

# Ubuntu/Debian
sudo apt install mysql-server

# Windows
# Download from mysql.com
```

### 2. Create Database

```bash
mysql -u root -p
CREATE DATABASE omnipresence CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'omnipresence'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON omnipresence.* TO 'omnipresence'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Backend Setup

```bash
cd apps/api

# Install Python dependencies
poetry install

# Copy environment file
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
poetry run python manage.py migrate

# Create admin user
poetry run python manage.py createsuperuser

# Load optional sample data
poetry run python manage.py loaddata sample_data

# Run development server
poetry run python manage.py runserver
```

### 4. Frontend Setup

```bash
cd apps/web

# Install dependencies
npm install

# Copy environment file
cp .env.example .env
# Edit .env if needed (default API URL is http://localhost:8000)

# Run dev server
npm run dev
```

---

## Project Structure

```
omnipresence/
├── apps/
│   ├── api/                 # Backend (Django REST)
│   │   ├── app/
│   │   │   ├── api/         # API endpoints
│   │   │   ├── models/      # Django models
│   │   │   ├── services/    # Business logic
│   │   │   └── core/        # Config, middleware
│   │   ├── manage.py
│   │   └── pyproject.toml
│   │
│   └── web/                 # Frontend (React + Vite)
│       ├── src/
│       │   ├── components/  # React components
│       │   ├── pages/       # Page components
│       │   ├── api/         # API client
│       │   └── store/       # Zustand stores
│       ├── package.json
│       └── vite.config.js
│
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=mysql://omnipresence:password@localhost:3306/omnipresence

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173

# Optional: External services
# REDIS_URL=redis://localhost:6379/0
# EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

### Frontend (.env)

```bash
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Omnipresence
```

---

## Common Commands

### Backend

```bash
cd apps/api

# Run development server
poetry run python manage.py runserver

# Run migrations
poetry run python manage.py migrate

# Create new migration
poetry run python manage.py makemigrations

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov

# Open Django shell
poetry run python manage.py shell

# Create superuser
poetry run python manage.py createsuperuser
```

### Frontend

```bash
cd apps/web

# Run dev server
npm run dev

# Run tests
npm run test

# Run tests with UI
npm run test:ui

# Build for production
npm run build

# Preview production build
npm run preview
```

### Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Run commands in container
docker-compose exec api python manage.py migrate
docker-compose exec web npm test
```

---

## Running Tests

### Backend Tests

```bash
cd apps/api

# Run all tests
poetry run pytest

# Run specific test file
poetry run pytest tests/test_presence.py

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Frontend Tests

```bash
cd apps/web

# Run unit tests
npm run test

# Run E2E tests
npm run test:e2e

# Run E2E tests with UI
npx playwright test --ui
```

---

## Code Style

### Backend (Python)

```bash
# Format code
poetry run black app/

# Check formatting
poetry run black --check app/

# Sort imports
poetry run isort app/

# Lint
poetry run flake8 app/

# Type checking (optional)
poetry run mypy app/
```

### Frontend (TypeScript)

```bash
# Format code
npm run format

# Check formatting
npm run format:check

# Lint
npm run lint

# Type check
npm run type-check
```

---

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
python manage.py runserver 8001
```

### MySQL Connection Issues

```bash
# Check MySQL is running
brew services list  # macOS
sudo systemctl status mysql  # linux

# Connect to MySQL
mysql -u root -p

# Check user permissions
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'omnipresence'@'localhost';
```

### Frontend Build Issues

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
npm run dev -- --force
```

### Migration Conflicts

```bash
# Reset migrations (development only!)
poetry run python manage.py migrate --fake-initial

# Or reset completely
DROP DATABASE omnipresence;
CREATE DATABASE omnipresence;
poetry run python manage.py migrate
```

---

## Useful Links

| Service            | URL                             |
|--------------------|---------------------------------|
| Frontend           | http://localhost:5173           |
| Backend API        | http://localhost:8000/api/      |
| API Docs (Swagger) | http://localhost:8000/api/docs/ |
| Django Admin       | http://localhost:8000/admin/    |
| Database           | localhost:3306                  |

---

## Next Steps

1. **Create admin user** for Django Admin access
2. **Load sample data** to explore the UI
3. **Read the architecture docs** to understand the codebase
4. **Set up your IDE** with Python and TypeScript support
5. **Join the team chat** for collaboration

---

## Getting Help

- Read [architecture.md](architecture.md) for system design
- Read [api-design.md](api-design.md) for API reference
- Read [database-schema.md](database-schema.md) for data model
- Check GitHub Issues for known problems
- Contact the development team
