# Dockerfile
# Use official Python image with slim bookworm (Debian 12) base
FROM python:3.12.4-alpine as base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --user --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

# Runtime configuration (override with docker-compose or run command)
FROM base as production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--workers", "4", "main:app"]

# Development configuration
FROM base as development
ENV MODE=development
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]