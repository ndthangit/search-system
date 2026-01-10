# Use Python 3.11 slim image as base
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt supervisor

COPY . .

EXPOSE 8080

ENV SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8080 \
    SERVER_WORKERS=1 \
    SERVER_NAME=http://localhost:8080 \
    DEBUG=False

CMD ["supervisord", "-c", "supervisord.conf"]