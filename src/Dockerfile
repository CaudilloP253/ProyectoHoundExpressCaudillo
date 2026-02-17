# syntax=docker/dockerfile:1

# --- Base image ---
FROM python:3.13-slim AS base

# --- Builder stage: install dependencies ---
FROM base AS builder
WORKDIR /app

# Install system dependencies required for pip packages (e.g. psycopg2, Pillow, etc.)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file(s) first for better cache utilization
COPY --link requirements.txt ./

# Install Python dependencies with cache mount for pip
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-warn-script-location --disable-pip-version-check --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# --- Final stage ---
FROM base AS final
WORKDIR /app

# Create a non-root user and group
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --link . .

# Set permissions
RUN chown -R appuser:appgroup /app
USER appuser

# Expose the port (adjust if your app uses a different port)
EXPOSE 8000

# Set environment variables for security
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Default command (adjust as needed, e.g. for Gunicorn or Django's runserver)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
