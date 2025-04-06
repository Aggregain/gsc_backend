# Этап сборки
FROM python:3.12-slim-bullseye as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    cargo \
    && apt-get clean

WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Финальный этап
FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update && apt-get install -y \
    libpq5 \
    && apt-get clean

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

EXPOSE 8000