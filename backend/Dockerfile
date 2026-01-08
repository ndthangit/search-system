# Use Python 3.11 slim image as base
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV SERVER_HOST=0.0.0.0 \
    SERVER_PORT=8080 \
    SERVER_WORKERS=1 \
    SERVER_NAME=http://localhost:8080 \
    DEBUG=False

CMD ["python", "main.py"]
