# ============================================================
# Dockerfile для Stars Sky (Django + Gunicorn)
# ============================================================
FROM python:3.10-slim
	
# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevent Python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
	
# Системные зависимости для psycopg2 и Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*
	
# Рабочая директория
WORKDIR /app
	
# Установка Python-зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
	
# Копирование проекта
COPY . /app/
	
# Создание директорий для логов, статики и медиа
RUN mkdir -p /app/logs /app/staticfiles /app/media /app/templates && \
    touch /app/logs/django.log /app/logs/gunicorn-access.log /app/logs/gunicorn-error.log
	
# Сборка статики (нужен .env для settings)
COPY .env.example /app/.env
RUN python manage.py collectstatic --noinput || true
	
# Entrypoint
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
	
# Gunicorn слушает порт 8083
EXPOSE 8083
	
ENTRYPOINT ["/app/entrypoint.sh"]
	
