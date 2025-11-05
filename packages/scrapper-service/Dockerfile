# Dockerfile for scrapper-service-mock
FROM python:3.11-slim

WORKDIR /app

# Install git and SSH for private repository access
RUN apt-get update && \
    apt-get install -y git openssh-client && \
    rm -rf /var/lib/apt/lists/*

# Add GitHub to known_hosts to prevent SSH host verification errors
RUN mkdir -p ~/.ssh && \
    ssh-keyscan github.com >> ~/.ssh/known_hosts

# Copy requirements files
COPY packages/scrapper-service/pyproject.toml packages/scrapper-service/

# Copy source code
COPY packages/scrapper-service/src packages/scrapper-service/src

# Install dependencies
# Note: SSH keys should be mounted during build for private git dependencies
RUN --mount=type=ssh pip install --no-cache-dir ./packages/scrapper-service

# Run the scrapper service consumer
CMD ["python", "-m", "scrapper_service"]
