# 🐳 Stars Sky — Docker Deployment

**Архитектура:**
- **Nginx** — на хосте (порт 80)
- **Django + Gunicorn** — в Docker контейнере (порт 8083)
- **PostgreSQL** — в Docker контейнере (порт 6954 → 5432)

```
┌─────────────────────────────────────────────────────────┐
│  Host (Ubuntu 22.04)                                    │
│                                                         │
│  ┌──────────┐         ┌──────────────────────────┐     │
│  │  Nginx   │ :80     │  Docker                  │     │
│  │  (host)  │────────▶│  ┌────────┐ ┌────────┐  │     │
│  └──────────┘         │  │ Web    │ │ Postgres │  │     │
│                       │  │:8083   │◀│:5432     │  │     │
│                       │  │Django+ │ │         │  │     │
│                       │  │Gunicorn│ │         │  │     │
│                       │  └────────┘ └────────┘  │     │
│                       │     :8083      :6954     │     │
│                       └──────────────────────────┘     │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Быстрый старт

### 1. Подготовка

```bash
cd /home/cubinez85/stars_sky

# Остановить Gunicorn на хосте
sudo systemctl stop gunicorn-stars-sky
sudo systemctl disable gunicorn-stars-sky

# Остановить локальный PostgreSQL (если работает)
sudo systemctl stop postgresql
sudo systemctl disable postgresql
```

### 2. Настройка .env

```bash
# Скопировать Docker .env
cp .env.docker .env

# Отредактировать
nano .env
```

**Обязательно измените:**
- `SECRET_KEY` — сгенерируйте новый
- `DB_PASSWORD` — установите надёжный пароль

### 3. Запуск Docker

```bash
# Запустить контейнеры
docker compose up -d --build

# Проверить статус
docker compose ps

# Посмотреть логи
docker compose logs -f
```

### 4. Обновить Nginx

```bash
# Скопировать Docker конфиг
sudo cp deploy/nginx/stars_sky_docker.conf /etc/nginx/sites-available/stars_sky

# Найти путь к static volume
STATIC_PATH=$(docker volume inspect stars_sky_project_static_files --format '{{ .Mountpoint }}')
MEDIA_PATH=$(docker volume inspect stars_sky_project_media_files --format '{{ .Mountpoint }}')

# Обновить пути в конфиге
sudo sed -i "s|/var/lib/docker/volumes/stars_sky_project_static_files/_data/|$STATIC_PATH/|g" /etc/nginx/sites-available/stars_sky.conf
sudo sed -i "s|/var/lib/docker/volumes/stars_sky_project_media_files/_data/|$MEDIA_PATH/|g" /etc/nginx/sites-available/stars_sky.conf

# Перезапустить Nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Проверка

```bash
# API
curl http://stars-sky.cubinez.ru/api/constellations/

# Звёздное небо
curl -I http://stars-sky.cubinez.ru/sky/

# Админка (логин: admin, пароль: admin)
# http://stars-sky.cubinez.ru/admin/
```

---

## 📋 Автоматическая миграция

Используйте скрипт для автоматической миграции:

```bash
chmod +x deploy/migrate_to_docker.sh
sudo bash deploy/migrate_to_docker.sh
```

---

## 🛠 Управление Docker

Используйте скрипт `docker-manage.sh`:

```bash
chmod +x docker-manage.sh

# Запуск/остановка
./docker-manage.sh start
./docker-manage.sh stop
./docker-manage.sh restart
./docker-manage.sh rebuild

# Логи
./docker-manage.sh logs          # Логи Django
./docker-manage.sh logs db       # Логи PostgreSQL
./docker-manage.sh status        # Статус и ресурсы

# Django команды
./docker-manage.sh shell         # Django shell
./docker-manage.sh migrate       # Применить миграции
./docker-manage.sh makemigrations # Создать миграции
./docker-manage.sh collectstatic # Собрать статику
./docker-manage.sh createsuperuser # Создать суперпользователя
./docker-manage.sh loaddata      # Загрузить данные

# PostgreSQL
./docker-manage.sh dbshell       # PostgreSQL shell

# Бэкапы
./docker-manage.sh backup        # Создать бэкап
./docker-manage.sh restore backup.sql  # Восстановить из бэкапа

# Очистка
./docker-manage.sh clean         # Удалить всё (включая volumes)
```

---

## 🔌 Подключение к PostgreSQL

### Из хоста

```bash
# Через Docker exec
docker compose exec db psql -U cubinez85 stars_sky

# Или через psql на хосте (порт 6954)
psql -h localhost -p 6954 -U cubinez85 stars_sky
```

### Из другого контейнера

```bash
# В той же Docker сети
DB_HOST=db
DB_PORT=5432
```

---

## 📁 Volumes

| Volume | Путь в контейнере | Назначение |
|--------|-------------------|------------|
| `postgres_data` | `/var/lib/postgresql/data` | Данные PostgreSQL |
| `static_files` | `/app/staticfiles` | Статические файлы Django |
| `media_files` | `/app/media` | Загруженные файлы |
| `logs` | `/app/logs` | Логи приложения |

### Найти путь к volume

```bash
docker volume inspect stars_sky_project_static_files --format '{{ .Mountpoint }}'
```

---

## 🔄 Обновление кода

```bash
# 1. Остановить контейнеры
docker compose down

# 2. Обновить код (git pull или копирование файлов)
git pull

# 3. Пересобрать и запустить
docker compose up -d --build

# 4. Применить миграции (если были изменения моделей)
docker compose exec web python manage.py migrate

# 5. Собрать статику (если были изменения)
docker compose exec web python manage.py collectstatic --noinput
```

---

## 📊 Мониторинг

```bash
# Логи в реальном времени
docker compose logs -f web

# Статус контейнеров
docker compose ps

# Использование ресурсов
docker stats

# Проверить здоровье
docker compose ps | grep healthy
```

---

## 🗄️ Бэкапы

### Автоматический бэкап

```bash
# Создать бэкап
./docker-manage.sh backup

# Бэкап сохранится в текущей директории
ls -lh backup_*.sql
```

### Восстановление

```bash
# Восстановить из бэкапа
./docker-manage.sh restore backup_20240101_120000.sql
```

### Cron для автоматических бэкапов

```bash
# Добавить в crontab
crontab -e

# Бэкап каждый день в 3:00
0 3 * * * cd /home/cubinez85/stars_sky && /home/cubinez85/stars_sky/docker-manage.sh backup
```

---

## 🔧 Отладка

### Контейнер не запускается

```bash
# Посмотреть логи
docker compose logs web

# Проверить здоровье PostgreSQL
docker compose logs db

# Перезапустить
docker compose restart web
```

### Ошибка подключения к БД

```bash
# Проверить что PostgreSQL работает
docker compose ps db

# Проверить переменные окружения
docker compose exec web env | grep DB_

# Проверить подключение
docker compose exec web python -c "
import os
import psycopg2
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    dbname=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD')
)
print('✅ Подключение успешно!')
conn.close()
"
```

### Статика не загружается

```bash
# Проверить что статика собрана
docker compose exec web ls -la /app/staticfiles/

# Пересобрать
docker compose exec web python manage.py collectstatic --noinput

# Проверить путь в Nginx
STATIC_PATH=$(docker volume inspect stars_sky_project_static_files --format '{{ .Mountpoint }}')
echo "Static path: $STATIC_PATH"
ls -la $STATIC_PATH
```

---

## 📝 Переменные окружения

| Переменная | Описание | По умолчанию |
|------------|----------|--------------|
| `SECRET_KEY` | Секретный ключ Django | (обязательно) |
| `DEBUG` | Режим отладки | `False` |
| `ALLOWED_HOSTS` | Разрешённые хосты | `localhost` |
| `DB_NAME` | Имя базы данных | `stars_sky` |
| `DB_USER` | Пользователь БД | `cubinez85` |
| `DB_PASSWORD` | Пароль БД | (обязательно) |
| `DB_HOST` | Хост БД | `db` (в Docker) |
| `DB_PORT` | Порт БД | `5432` |
| `CORS_ALLOWED_ORIGINS` | CORS origins | (опционально) |

---

## 🎯 Порты

| Сервис | Порт на хосте | Порт в контейнере |
|--------|---------------|-------------------|
| Nginx | 80 | — (на хосте) |
| Django/Gunicorn | 8083 | 8083 |
| PostgreSQL | 6954 | 5432 |

---

## ✅ Чек-лист

- [ ] Остановить Gunicorn на хосте
- [ ] Остановить локальный PostgreSQL
- [ ] Скопировать `.env.docker` в `.env`
- [ ] Изменить `SECRET_KEY` и `DB_PASSWORD` в `.env`
- [ ] Запустить `docker compose up -d --build`
- [ ] Обновить Nginx конфиг
- [ ] Проверить работу API
- [ ] Проверить админку
- [ ] Настроить автоматические бэкапы

---

## 🆘 Полезные команды

```bash
# Полная перезагрузка
docker compose down -v
docker compose up -d --build

# Войти в контейнер
docker compose exec web bash

# Выполнить команду в контейнере
docker compose exec web python manage.py <command>

# Посмотреть использование диска
docker system df

# Очистить неиспользуемые образы
docker image prune -f

# Посмотреть все volumes
docker volume ls
```

---

Удачи с Docker! 🐳✨
