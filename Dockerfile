# Stage 1: Build stage
FROM python:3.12-slim AS builder

# Установка Python-зависимостей
WORKDIR /app
COPY requirements.txt .

# Установка системных зависимостей (если нужны)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* && \
    pip install --user --no-cache-dir -r requirements.txt 

# Копирование исходного кода
COPY app.py .

# Stage 2: Final stage
FROM python:3.12-slim

# Установка только runtime-зависимостей (если нужны)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*
# Копирование установленных Python-зависимостей из builder-стадии
WORKDIR /app
COPY --from=builder /root/.local /root/.local

# Копирование исходного кода из builder-стадии  
COPY --from=builder /app/app.py .

# Установка PATH для доступа к пользовательским пакетам
ENV PATH=/root/.local/bin:$PATH

# Команда для запуска приложения через Gunicorn
ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
