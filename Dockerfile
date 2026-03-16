## Multi-stage optimized Dockerfile: build wheels in a builder stage, install only wheels in final image
FROM python:3.10-slim AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /wheels

# Build deps for some geospatial packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc git gdal-bin libgdal-dev libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --upgrade pip setuptools wheel \
  && pip wheel --wheel-dir /wheels -r requirements.txt

FROM python:3.10-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Minimal runtime deps (keep required system libs for geospatial runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin libgdal-dev libpq-dev ca-certificates \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy wheels and install (no build tools required)
COPY --from=builder /wheels /wheels
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user for security
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

# Default entrypoint (override at runtime)
CMD ["python", "-m", "src.optimize", "--config", "experiments/configs/experiment_01.yaml"]
