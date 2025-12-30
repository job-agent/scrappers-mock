# Scrappers Mock

Mock scrapper service for the Job Agent platform. This service provides fabricated job listings for development, integration testing, and public demonstrations without requiring access to real job scraping providers.

## Overview

The scrappers-mock service implements the same `ScrapperServiceInterface` as the production scrapper, communicating via RabbitMQ with the job-agent-platform. It returns predefined mock job listings generated using Faker, enabling end-to-end testing of the job processing pipeline without external dependencies.

**Key features:**

- Contract-compatible with production scrappers (uses `shared/job-scrapper-contracts`)
- RabbitMQ-based communication (uses `shared/scrapper-messaging`)
- Deterministic schema with dynamic identifiers via Faker
- Docker-ready for easy deployment
- Interchangeable with real scrappers at runtime

## Directory Structure

```
scrappers-mock/
├── packages/
│   └── scrapper-service/           # Main service package
│       ├── src/
│       │   └── scrapper_service/
│       │       ├── __init__.py     # Package exports
│       │       ├── __main__.py     # CLI entry point
│       │       ├── manager.py      # ScrapperManager implementation
│       │       └── jobs_data.py    # Mock job data generator
│       ├── Dockerfile              # Container build file
│       └── pyproject.toml          # Package configuration
├── scripts/
│   ├── reinstall_packages.sh       # Reinstall all packages
│   ├── lint_and_format.sh          # Run ruff linter/formatter
│   ├── create-worktree.sh          # Create git worktree for development
│   └── delete-worktree.sh          # Clean up git worktree
├── smoke_tests/
│   ├── conftest.py                 # Pytest fixtures
│   └── test_type_checking.py       # Type checking smoke tests
├── .github/
│   └── workflows/
│       └── ci.yml                  # CI pipeline (lint, smoke tests, Docker)
├── docker-compose.yml              # Service deployment configuration
├── pyproject.toml                  # Root project configuration
├── .env.example                    # Environment variables template
└── README.md                       # This file
```

## Prerequisites

- Python 3.9+
- Docker and Docker Compose
- Running infrastructure (PostgreSQL, RabbitMQ) from the `infrastructure/` directory

## Quick Start

### 1. Start Infrastructure

Before running the mock scrapper, ensure the shared infrastructure is running:

```bash
cd ../infrastructure
docker compose up -d
```

### 2. Configure Environment

Copy the environment template and adjust if needed:

```bash
cp .env.example .env
```

Default configuration:

```
RABBITMQ_USER=jobagent
RABBITMQ_PASSWORD=jobagent
RABBITMQ_VHOST=/
RABBITMQ_PORT=5672
RABBITMQ_URL=amqp://jobagent:jobagent@localhost:5672/
```

### 3. Run with Docker (Recommended)

```bash
docker compose up -d
```

The service connects to the `job-agent-network` external network and communicates with RabbitMQ at `job-agent-rabbitmq:5672`.

### 4. Run Locally (Development)

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
./scripts/reinstall_packages.sh

# Run the service
python -m scrapper_service --rabbitmq-url amqp://jobagent:jobagent@localhost:5672/
```

## CLI Options

```bash
python -m scrapper_service [OPTIONS]

Options:
  --rabbitmq-url TEXT       RabbitMQ connection URL (default: from RABBITMQ_URL env var)
  --log-level [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                            Logging level (default: INFO)
  --check                   Check that the service can start (for CI/testing)
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `RABBITMQ_URL` | Full RabbitMQ connection URL | `amqp://jobagent:jobagent@localhost:5672/` |
| `RABBITMQ_USER` | RabbitMQ username | `jobagent` |
| `RABBITMQ_PASSWORD` | RabbitMQ password | `jobagent` |
| `RABBITMQ_VHOST` | RabbitMQ virtual host | `/` |

### Docker Compose Configuration

The service uses an external Docker network (`job-agent-network`) created by the infrastructure stack. The RabbitMQ URL in Docker uses the container hostname `job-agent-rabbitmq`.

## Integration with Job Agent Platform

### Switching Between Real and Mock Scrappers

The mock scrapper is interchangeable with the real scrapper service. To switch:

```bash
# Stop real scrapper
cd ../scrappers && docker compose down

# Start mock scrapper
cd ../scrappers-mock && docker compose up -d

# Or reverse to use real scrapper
```

Both services implement the `ScrapperServiceInterface` from `shared/job-scrapper-contracts` and communicate via the same RabbitMQ queues, making them transparent to the job-agent-platform.

### Communication Flow

1. **job-agent-platform** sends scrape requests to the `job.scrape.request` queue
2. **scrappers-mock** receives requests via `ScrapperConsumer` (from `scrapper-messaging`)
3. `ScrapperManager.scrape_jobs()` generates mock job listings
4. Results are returned via the reply queue

### Dependencies

- **shared/job-scrapper-contracts**: Shared data models (`Job`, `Company`, `Salary`, `Location`, `ScrapeJobsFilter`)
- **shared/scrapper-messaging**: RabbitMQ consumer/producer utilities (`ScrapperConsumer`)

Both dependencies are fetched from public GitHub repositories during installation.

## Mock Data

The service generates 10 diverse mock job listings covering various roles:

- Backend Engineer (Python / FastAPI)
- Full-stack Engineer (Node.js / Nest.js / React)
- DevOps Engineer (AWS / Kubernetes)
- Frontend Developer (React / TypeScript)
- AI Research Engineer
- Product Manager (EdTech)
- AI Engineer (Python / LangChain / LangGraph)
- UX/UI Designer
- Customer Success Manager
- Marketing Copywriter

Each job includes:
- Dynamic identifiers generated by Faker
- Realistic descriptions and requirements
- Salary ranges (USD)
- Location with remote/on-site flags
- Experience requirements
- Industry classification

## Development

### Installing Dependencies

```bash
./scripts/reinstall_packages.sh
```

### Linting and Formatting

```bash
./scripts/lint_and_format.sh
```

This runs `ruff check --fix` followed by `ruff format`.

### Running Tests

```bash
# Run smoke tests (type checking)
pytest -m smoke -v smoke_tests/

# Run all tests
pytest
```

### Type Checking

```bash
cd packages/scrapper-service
mypy src/scrapper_service --ignore-missing-imports
```

## CI Pipeline

The GitHub Actions workflow (`.github/workflows/ci.yml`) runs on pushes and PRs to `main` and `development` branches:

1. **Lint**: Runs ruff check and format verification
2. **Smoke Tests**: Installs packages and runs mypy type checking
3. **Docker Startup Test**: Builds the Docker image and verifies container startup

## License

Internal use only. Part of the Job Agent platform monorepo.
