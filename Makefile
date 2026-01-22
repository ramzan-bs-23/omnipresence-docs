.PHONY: help dev dev.backend dev.frontend build test test.backend test.frontend clean docker.up docker.down docker.logs

help:
	@echo "Available commands:"
	@echo "  make dev           - Start development servers (backend and frontend)"
	@echo "  make dev.backend   - Start Django backend server"
	@echo "  make dev.frontend  - Start React frontend server"
	@echo "  make build         - Build frontend for production"
	@echo "  make test          - Run all tests"
	@echo "  make test.backend  - Run backend tests"
	@echo "  make test.frontend - Run frontend tests"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make docker.up     - Start Docker services"
	@echo "  make docker.down   - Stop Docker services"
	@echo "  make docker.logs   - Show Docker logs"

dev:
	@make -j2 dev.backend dev.frontend

dev.backend:
	@echo "Starting Django backend..."
	@cd apps/api && python manage.py runserver

dev.frontend:
	@echo "Starting React frontend..."
	@cd apps/web && npm run dev

build:
	@echo "Building frontend..."
	@cd apps/web && npm run build

test:
	@make test.backend test.frontend

test.backend:
	@echo "Running backend tests..."
	@cd apps/api && pytest

test.frontend:
	@echo "Running frontend tests..."
	@cd apps/web && npm run test

clean:
	@echo "Cleaning build artifacts..."
	@cd apps/web && rm -rf dist node_modules/.vite
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

docker.up:
	@echo "Starting Docker services..."
	@docker-compose up -d

docker.down:
	@echo "Stopping Docker services..."
	@docker-compose down

docker.logs:
	@docker-compose logs -f
