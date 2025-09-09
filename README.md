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
```

- Запуск:
```bash
docker compose up --build -d
```

- Документация API: http://localhost:8000/docs

Примечания:
- Контейнеры: `backend` (FastAPI, порт 8000), `db` (Postgres, порт 5432), `redis` (порт 6379).
- Переменные берутся из `.env` автоматически (см. `docker-compose.yml`).

## 2) Как запустить скрипт подписчика listener.py

Скрипт `listener.py` слушает Redis-канал `image_channel` и печатает события загрузки.

- Через uv (рекомендуется):
```bash
uv run python listener.py
```

- Без uv (через обычный venv/pip):
```bash
# создать и активировать виртуальное окружение
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

# установить зависимости (минимум, чтобы запустить listener)
pip install redis fastapi pydantic-settings aiofiles alembic asyncpg

# запустить подписчика
python listener.py
```

- Параметры подключения в `listener.py` по умолчанию:
  - Redis: `localhost:6379` (это корректно, если `docker compose` пробрасывает порт Redis на хост)
  - Канал: `image_channel`

Если Redis в другом месте: отредактируйте `listener.py` (host/port) или задайте переменные окружения и читайте их в скрипте.

## 3) Минимальные примеры запросов (curl)

- Загрузка изображения (multipart/form-data):
```bash
curl -X POST "http://localhost:8000/api/v1/images/" \
  -F "title=My title" \
  -F "description=Short desc" \
  -F "file=@/path/to/image.jpg;type=image/jpeg"
```
Ответ (пример):
```json
{
  "id": "<uuid>",
  "title": "My title",
  "description": "Short desc",
  "filename": "image.jpg",
  "created_at": "2025-09-09T18:09:00+00:00",
  "updated_at": "2025-09-09T18:09:00+00:00",
  "file_url": "uploads/<uuid>.jpg"
}
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

