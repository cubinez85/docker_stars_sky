#!/bin/bash
# ============================================================
# Docker management script для Stars Sky
# ============================================================

PROJECT_DIR="/home/cubinez85/stars_sky"
cd "$PROJECT_DIR"

case "$1" in
    start)
        echo "🚀 Запуск контейнеров..."
        docker compose up -d
        ;;
    stop)
        echo "🛑 Остановка контейнеров..."
        docker compose down
        ;;
    restart)
        echo "🔄 Перезапуск контейнеров..."
        docker compose restart
        ;;
    rebuild)
        echo "🔨 Пересборка и запуск..."
        docker compose up -d --build
        ;;
    logs)
        echo "📋 Логи (Ctrl+C для выхода)..."
        docker compose logs -f ${2:-web}
        ;;
    status)
        echo "📊 Статус контейнеров:"
        docker compose ps
        echo ""
        echo "📊 Использование ресурсов:"
        docker stats --no-stream
        ;;
    shell)
        echo "🐚 Django shell..."
        docker compose exec web python manage.py shell
        ;;
    dbshell)
        echo "🗄️  PostgreSQL shell..."
        docker compose exec db psql -U cubinez85 stars_sky
        ;;
    migrate)
        echo "🔄 Применение миграций..."
        docker compose exec web python manage.py migrate
        ;;
    makemigrations)
        echo "📝 Создание миграций..."
        docker compose exec web python manage.py makemigrations
        ;;
    collectstatic)
        echo "🎨 Сборка статики..."
        docker compose exec web python manage.py collectstatic --noinput
        ;;
    createsuperuser)
        echo "👤 Создание суперпользователя..."
        docker compose exec web python manage.py createsuperuser
        ;;
    loaddata)
        echo "📊 Загрузка начальных данных..."
        docker compose exec web python manage.py load_initial_data
        ;;
    backup)
        echo "💾 Создание бэкапа БД..."
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        docker compose exec -T db pg_dump -U cubinez85 stars_sky > "$BACKUP_FILE"
        echo "✅ Бэкап создан: $BACKUP_FILE"
        ;;
    restore)
        if [ -z "$2" ]; then
            echo "❌ Укажите файл бэкапа: $0 restore backup.sql"
            exit 1
        fi
        echo "📥 Восстановление из $2..."
        docker compose exec -T db psql -U cubinez85 stars_sky < "$2"
        echo "✅ Бэкап восстановлен"
        ;;
    clean)
        echo "🧹 Очистка неиспользуемых образов..."
        docker compose down -v
        docker system prune -f
        echo "✅ Очистка завершена"
        ;;
    *)
        echo "🌌 Stars Sky — Docker Management"
        echo ""
        echo "Использование: $0 {command}"
        echo ""
        echo "Команды:"
        echo "  start           - Запуск контейнеров"
        echo "  stop            - Остановка контейнеров"
        echo "  restart         - Перезапуск контейнеров"
        echo "  rebuild         - Пересборка и запуск"
        echo "  logs [service]  - Просмотр логов (web/db)"
        echo "  status          - Статус и ресурсы"
        echo "  shell           - Django shell"
        echo "  dbshell         - PostgreSQL shell"
        echo "  migrate         - Применение миграций"
        echo "  makemigrations  - Создание миграций"
        echo "  collectstatic   - Сборка статики"
        echo "  createsuperuser - Создание суперпользователя"
        echo "  loaddata        - Загрузка начальных данных"
        echo "  backup          - Бэкап базы данных"
        echo "  restore <file>  - Восстановление из бэкапа"
        echo "  clean           - Полная очистка (включая volumes)"
        echo ""
        ;;
esac
