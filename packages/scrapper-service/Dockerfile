# Dockerfile for scrapper-service-mock
FROM python:3.11-slim

WORKDIR /app

# Install git for fetching dependencies from public GitHub repos
RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY packages/scrapper-service/pyproject.toml packages/scrapper-service/

# Copy source code
COPY packages/scrapper-service/src packages/scrapper-service/src

# Install dependencies (public repos, no auth needed)
RUN pip install --no-cache-dir ./packages/scrapper-service

# Run the scrapper service consumer
CMD ["python", "-m", "scrapper_service"]
