---
title: Docker Deployment
description: Run Nexus Core in Docker containers. Consistent, portable, production-ready.
section: deployments
order: 1
---

# Docker Deployment

Run Nexus Core in **Docker containers**. Consistent, portable, production-ready.

## Quick Start

```bash
# Pull image
docker pull skillseekers/nexus-core:latest

# Run scrape
docker run -v $(pwd):/data skillseekers/nexus-core:latest \
  scrape --config /data/config.json
```

## Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install nexus-core

# Copy configs
COPY configs/ /app/configs/

# Default command
CMD ["nexus-core", "--help"]
```

## Docker Compose

```yaml
version: '3.8'

services:
  nexus-core:
    image: skillseekers/nexus-core:latest
    volumes:
      - ./configs:/app/configs
      - ./output:/app/output
      - ./.env:/app/.env
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - GITHUB_TOKEN=${GITHUB_TOKEN}
    command: scrape --config /app/configs/react.json
```

## Build Custom Image

```bash
# Build
docker build -t my-nexus-core .

# Run
docker run -v $(pwd)/output:/app/output my-nexus-core \
  scrape --config configs/react.json
```

## CI/CD Pipeline

```yaml
# .github/workflows/skills.yml
name: Update Skills

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Skills
        run: |
          docker run -v $(pwd):/data \
            skillseekers/nexus-core:latest \
            scrape --config /data/configs/react.json
```

## Features

- ✅ **Consistent environment** - Same Python version everywhere
- ✅ **Portable** - Run anywhere Docker runs
- ✅ **Isolated** - No system dependencies
- ✅ **CI/CD ready** - Perfect for GitHub Actions
