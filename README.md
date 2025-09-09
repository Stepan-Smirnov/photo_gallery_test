# Photo Gallery (FastAPI)

Сервис на FastAPI для загрузки изображений. Хранение — Postgres, кеш/события — Redis.

## 1) Запуск проекта через Docker

Требования: Docker, Docker Compose.

- Создайте файл `.env` в корне (можно скопировать из примера):
```bash
cp env.docker.example .env   # macOS/Linux
# или PowerShell
copy env.docker.example .env
```

- Пример содержимого `.env` (можно менять по необходимости):
```env
# PostgreSQL
DB_HOST=db
DB_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres_password

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_CHANNEL=image_channel
```

- Запуск:
```bash
docker compose up -d
```

- Документация API: http://localhost:8000/docs

Примечания:
- Контейнеры: `backend` (FastAPI, порт 8000), `db` (Postgres, порт 5432), `redis` (порт 6379).
- Переменные берутся из `.env` автоматически (см. `docker-compose.yml`).

## 2) Как запустить скрипт подписчика listener.py

Скрипт `listener.py` не читает .env и по умолчанию подключается к Redis `localhost:6379`, канал `image_channel`.

- Через uv:
```bash
uv sync
uv run python listener.py
```

- Без uv (через обычный venv/pip):
```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install redis
python listener.py
```

Если ваш Redis не на localhost, отредактируйте хост/порт и канал прямо в `listener.py`.

## 3) Минимальные примеры запросов (curl)

- Загрузка изображения (multipart/form-data):
```bash
curl -X POST "http://localhost:8000/api/v1/images/" \
  -F "title=My title" \
  -F "description=Short desc" \
  -F "file=@/path/to/image.jpg;type=image/jpeg"
```

- Получить изображение по id:
```bash
curl "http://localhost:8000/api/v1/images/<uuid>"
```

- Обновить только заголовок/описание (PATCH):
```bash
curl -X PATCH "http://localhost:8000/api/v1/images/<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New title","description":"New desc"}'
```

- Удалить по id:
```bash
curl -X DELETE "http://localhost:8000/api/v1/images/<uuid>"
```

## 4) Структура таблицы в БД

Таблица `images`:
- `id` UUID PRIMARY KEY
- `title` VARCHAR(32) UNIQUE NOT NULL
- `description` VARCHAR(32) NOT NULL
- `filename` VARCHAR(128) NOT NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT now()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT now()  
  (в ORM поле обновляется на апдейте через `onupdate=func.now()`)
- `file_url` VARCHAR(128) NOT NULL

