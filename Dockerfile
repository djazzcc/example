FROM python:3.13-alpine AS builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN set -eux; \
    apk add --no-cache  && \
    pip install --no-cache-dir --no-deps --upgrade pip && \
    pip install --no-cache-dir uv

COPY pyproject.toml /pyproject.toml

RUN set -eux; \
    uv pip compile --upgrade pyproject.toml -o /requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r /requirements.txt


FROM python:3.13-alpine AS runner
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /wheels /wheels
RUN set -eux; \
    apk add --no-cache bash && \
    pip install --no-cache-dir --no-deps /wheels/* && \
    rm -rf /wheels

WORKDIR /app
COPY . /app
EXPOSE 8000

COPY ./scripts/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]
CMD ["gunicorn"]