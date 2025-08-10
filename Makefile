## Makefile for Talk‑To‑DB

.PHONY: help init build-docker start-docker stop-docker shell-docker

help:
	@echo "Available targets:"
	@echo "  init          Install Python dependencies for local development"
	@echo "  build-docker  Build all Docker images (backend & frontend)"
	@echo "  start-docker  Start the full stack using docker-compose"
	@echo "  stop-docker   Stop the stack and remove volumes"
	@echo "  shell-docker  Open a bash shell in the backend container"

# Install Python deps locally for testing (virtualenv recommended)
init:
	pip install -r backend/requirements.txt

# Build images using docker compose
build-docker:
	docker compose build

# Start services in detached mode
start-docker:
	docker compose up -d

# Stop services and remove volumes
stop-docker:
	docker compose down -v

# Exec into backend container for debugging
shell-docker:
	docker compose exec backend bash