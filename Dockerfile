# syntax=docker/dockerfile:1.7
FROM python:3.13-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VERSION=1.8.3 \
    PATH="/root/.local/bin:$PATH"
WORKDIR /app

FROM base AS builder
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy Poetry files from backend/
COPY backend/pyproject.toml backend/poetry.lock /app/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-interaction --no-ansi

# Copy Python package from backend/app -> /app/app
COPY backend/app /app/app

FROM python:3.13-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UVICORN_WORKERS=2 \
    PORT=8000
WORKDIR /app
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app/app /app/app

RUN useradd -u 10001 -m appuser
USER appuser

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request,sys,os; urllib.request.urlopen(f'http://127.0.0.1:{os.getenv(\"PORT\",\"8000\")}/healthz'); sys.exit(0)"

CMD exec uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT} --workers ${UVICORN_WORKERS}
