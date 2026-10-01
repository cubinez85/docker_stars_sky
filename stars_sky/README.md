# 🌌 Stars Sky — Интерактивная модель звёздного неба

**Backend:** Django 4.2 + Django REST Framework
**База данных:** PostgreSQL
**Сервер:** Nginx (порт 80) → Gunicorn (порт 8083)
**ОС:** Ubuntu 22.04

---

## 📁 Структура проекта

```
/home/cubinez85/stars_sky/
├── manage.py                    # Точка входа Django
├── requirements.txt             # Python-зависимости
├── .env                         # Переменные окружения (НЕ в git!)
├── .env.example                 # Шаблон .env
├── stars_sky/                   # Настройки проекта
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── constellations/              # Приложение «Созвездия»
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── admin.py
│   ├── migrations/
│   └── management/commands/
│       └── load_initial_data.py
├── stars/                       # Приложение «Звёзды»
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   └── admin.py
├── deploy/
│   ├── deploy.sh                # Скрипт автоматического развёртывания
│   ├── nginx/
│   │   └── stars_sky.conf       # Конфиг Nginx
│   └── systemd/
│       └── gunicorn-stars-sky.service  # Unit-файл Gunicorn
├── logs/                        # Логи
├── staticfiles/                 # Собранные статики
├── media/                       # Загруженные файлы
└── templates/                   # HTML-шаблоны
```

---

## 🚀 Быстрый старт (развёртывание)

### 1. Клонировать проект

```bash
cd /home/cubinez85
git clone <your-repo-url> stars_sky
cd stars_sky
```

### 2. Запустить скрипт развёртывания

```bash
chmod +x deploy/deploy.sh
sudo bash deploy/deploy.sh
```

Скрипт автоматически:
- Установит системные пакеты (Python, PostgreSQL, Nginx)
- Создаст базу данных PostgreSQL
- Установит Python-зависимости в venv
- Выполнит миграции
- Настроит Nginx и systemd

### 3. Отредактировать .env

```bash
nano /home/cubinez85/stars_sky/.env
```

Обязательно сменить:
- `SECRET_KEY` — сгенерировать новый
- `DB_PASSWORD` — пароль для PostgreSQL
- `ALLOWED_HOSTS` — домен сервера

### 4. Создать суперпользователя

```bash
cd /home/cubinez85/stars_sky
/var/www/automatic_database_backup/venv/bin/python manage.py createsuperuser
```

### 5. Проверить

```bash
# Статус Gunicorn
sudo systemctl status gunicorn-stars-sky

# Статус Nginx
sudo systemctl status nginx

# Логи
sudo journalctl -u gunicorn-stars-sky -f
tail -f /home/cubinez85/stars_sky/logs/django.log
```

---

## 🔌 API Endpoints

### Созвездия

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/constellations/` | Список всех созвездий |
| POST | `/api/constellations/` | Создать созвездие |
| GET | `/api/constellations/{id}/` | Детали созвездия |
| PUT | `/api/constellations/{id}/` | Полное обновление |
| PATCH | `/api/constellations/{id}/` | Частичное обновление |
| DELETE | `/api/constellations/{id}/` | Удалить |

**Фильтры:** `?is_zodiacal=true&best_viewing_month=6`
**Поиск:** `?search=Орион`
**Сортировка:** `?ordering=-name_ru`

### Звёзды

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/stars/` | Список всех звёзд |
| POST | `/api/stars/` | Создать звезду |
| GET | `/api/stars/{id}/` | Детали звезды |
| PUT | `/api/stars/{id}/` | Полное обновление |
| PATCH | `/api/stars/{id}/` | Частичное обновление |
| DELETE | `/api/stars/{id}/` | Удалить |

**Фильтры:** `?constellation=1&spectral_class=G&is_variable=true`
**Поиск:** `?search=Бетельгейзе`
**Сортировка:** `?ordering=apparent_magnitude`

---

## 🛠 Ручная установка (без скрипта)

### Системные зависимости

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx
```

### PostgreSQL

```bash
sudo -u postgres psql
```

```sql
CREATE DATABASE stars_sky;
CREATE ROLE cubinez85 WITH LOGIN PASSWORD 'ваш_пароль';
GRANT ALL PRIVILEGES ON DATABASE stars_sky TO cubinez85;
ALTER DATABASE stars_sky OWNER TO cubinez85;
\q
```

### Python-зависимости

```bash
cd /home/cubinez85/stars_sky
/var/www/automatic_database_backup/venv/bin/pip install -r requirements.txt
```

### Миграции и данные

```bash
cd /home/cubinez85/stars_sky
/var/www/automatic_database_backup/venv/bin/python manage.py makemigrations
/var/www/automatic_database_backup/venv/bin/python manage.py migrate
/var/www/automatic_database_backup/venv/bin/python manage.py collectstatic --noinput
/var/www/automatic_database_backup/venv/bin/python manage.py load_initial_data
```

### Nginx

```bash
sudo cp deploy/nginx/stars_sky.conf /etc/nginx/sites-available/stars_sky
sudo ln -sf /etc/nginx/sites-available/stars_sky /etc/nginx/sites-enabled/stars_sky
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

### Systemd (Gunicorn)

```bash
sudo cp deploy/systemd/gunicorn-stars-sky.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable gunicorn-stars-sky
sudo systemctl restart gunicorn-stars-sky
```

---

## ⚙️ Полезные команды

```bash
# Перезапуск Gunicorn
sudo systemctl restart gunicorn-stars-sky

# Перезагрузка Nginx
sudo nginx -t && sudo systemctl reload nginx

# Просмотр логов Gunicorn
sudo journalctl -u gunicorn-stars-sky -f

# Просмотр логов Django
tail -f /home/cubinez85/stars_sky/logs/django.log

# Создание миграций
/var/www/automatic_database_backup/venv/bin/python manage.py makemigrations

# Применение миграций
/var/www/automatic_database_backup/venv/bin/python manage.py migrate

# Загрузка начальных данных
/var/www/automatic_database_backup/venv/bin/python manage.py load_initial_data

# Создание бэкапа БД
pg_dump stars_sky > backup_$(date +%Y%m%d).sql

# Восстановление БД
psql stars_sky < backup_20240101.sql
```

---

## 🔒 Безопасность

- [ ] Сменить `SECRET_KEY` в `.env`
- [ ] Установить надёжный `DB_PASSWORD`
- [ ] Указать реальный домен в `ALLOWED_HOSTS`
- [ ] Настроить HTTPS (Let's Encrypt / certbot)
- [ ] Ограничить доступ к `/admin/` по IP

---

## 📝 Лицензия

MIT
