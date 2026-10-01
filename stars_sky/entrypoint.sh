#!/bin/bash
# ============================================================
# Entrypoint для Stars Sky Docker контейнера
# ============================================================
set -e

echo "🌌 Stars Sky — Запуск контейнера..."

# Ждём PostgreSQL
echo "⏳ Ожидание PostgreSQL..."
MAX_RETRIES=60
RETRY_COUNT=0

while ! python -c "
import socket
import sys
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect(('db', 5432))
    s.close()
    sys.exit(0)
except Exception as e:
    print(f'Connection failed: {e}', file=sys.stderr)
    sys.exit(1)
" 2>/dev/null; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "❌ PostgreSQL не отвечает после $MAX_RETRIES попыток"
        echo "Проверка сетевой доступности:"
        getent hosts db || echo "  ❌ Хост 'db' не резолвится"
        exit 1
    fi
    echo "  PostgreSQL не готов, попытка $RETRY_COUNT/$MAX_RETRIES..."
    sleep 3
done

echo "✅ PostgreSQL доступен!"

# Применяем миграции
echo "🔄 Применение миграций..."
python manage.py migrate --noinput

# Загрузка начальных данных (если таблица пустая)
echo "📊 Проверка начальных данных..."
python manage.py load_initial_data || true

# Сборка статики
echo "🎨 Сборка статических файлов..."
python manage.py collectstatic --noinput

# Создаём суперпользователя если его нет
echo "👤 Проверка суперпользователя..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('  Создаём суперпользователя admin/admin...')
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
else:
    print('  Суперпользователь уже существует')
" || true

echo ""
echo "============================================"
echo "  🚀 Запуск Gunicorn на порту 8083"
echo "============================================"
echo ""

# Запуск Gunicorn
exec gunicorn stars_sky.wsgi:application \
    --bind 0.0.0.0:8083 \
    --workers 3 \
    --threads 2 \
    --worker-class gthread \
    --timeout 120 \
    --access-logfile /app/logs/gunicorn-access.log \
    --error-logfile /app/logs/gunicorn-error.log \
    --capture-output \
    --log-level info
