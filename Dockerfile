FROM python:3.13-alpine AS builder

ARG DEV=false
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install build dependencies
RUN set -eux; \
    apk add --no-cache  && \
    pip install --no-cache-dir --no-deps --upgrade pip && \
    pip install --no-cache-dir uv

COPY pyproject.toml /pyproject.toml

# Generate requirements based on build type
RUN set -eux; \
    if [ "$DEV" = "true" ] ; then \
        uv pip compile --upgrade --extra dev pyproject.toml -o /requirements.txt; \
    else \
        uv pip compile --upgrade pyproject.toml -o /requirements.txt; \
    fi && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /requirements.txt


FROM python:3.13-alpine AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install runtime dependencies
RUN apk add --no-cache \
    postgresql-libs \
    bash

COPY --from=builder /wheels /wheels
RUN set -eux; \
    apk add --no-cache bash && \
    pip install --no-cache-dir --no-deps /wheels/* && \
    rm -rf /wheels

WORKDIR /app
COPY . /app
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "djazz.wsgi:application"]