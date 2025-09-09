# Photo Gallery (FastAPI)

Небольшой сервис на FastAPI для загрузки изображений: принимает файл и метаданные, сохраняет в Postgres, кеширует ответы в Redis и публикует событие о загрузке.

## Запуск

### Вариант A — через Docker (рекомендуется)

Требования: Docker, Docker Compose.

1) Создайте .env на основе примера:
```bash
copy env.docker.example .env   # Windows PowerShell: cp env.docker.example .env
```
2) Запустите:
```bash
docker compose up --build
```
3) Откройте:
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json

Сервисы:
- backend: FastAPI на 8000
- db: Postgres 16 на 5432
- redis: Redis 7 на 6379

### Вариант B — локально (без Docker)

Требования: Python 3.12+, установлен `uv`.

1) Установка зависимостей:
```bash
uv sync --frozen
```
2) Создайте .env на основе примера:
```bash
copy env.local.example .env   # Windows PowerShell: cp env.local.example .env
```
3) Примените миграции и запустите сервер:
```bash
uv run alembic upgrade head
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
```
4) Документация: http://localhost:8000/docs

## API

Базовый префикс: `/api/v1`

- POST `/api/v1/images/` — загрузить изображение (multipart/form-data)
- GET `/api/v1/images/{id}` — получить по id
- GET `/api/v1/images/` — список
- PATCH `/api/v1/images/{id}` — частичное обновление метаданных
- DELETE `/api/v1/images/{id}` — удалить

## Примеры запросов

Загрузка изображения (curl):
```bash
curl -X POST "http://localhost:8000/api/v1/images/" \
  -F "title=My title" \
  -F "description=Short desc" \
  -F "file=@/path/to/image.jpg;type=image/jpeg"
```

Загрузка изображения (httpie):
```bash
http -f POST :8000/api/v1/images/ \
  title="My title" description="Short desc" \
  file@/path/to/image.jpg
```

Получить по id:
```bash
http :8000/api/v1/images/<uuid>
```

Список:
```bash
http :8000/api/v1/images/
```

Частичное обновление (PATCH):
```bash
http PATCH :8000/api/v1/images/<uuid> title="New title" description="New desc"
# или curl
curl -X PATCH "http://localhost:8000/api/v1/images/<uuid>" \
  -H "Content-Type: application/json" \
  -d '{"title":"New title","description":"New desc"}'
```

Удаление:
```bash
http DELETE :8000/api/v1/images/<uuid>
```

## События и кеш Redis

- При успешной загрузке публикуется событие в канал `image_channel` со структурой:
```json
{"event":"image_uploaded","id":"<uuid>","title":"..."}
```
- Кеш ответа по изображению хранится в ключе `image:<uuid>` 60 секунд.

### Как запустить listener.py

Скрипт `listener.py` подписывается на канал Redis и печатает события загрузки изображений.

- Локально (использует переменные из .env):
```bash
uv run python listener.py
```
- Явно указать адрес (пример для Docker Desktop на Windows):
```bash
$env:REDIS_HOST="localhost"; $env:REDIS_PORT="6379"; uv run python listener.py
```
При запуске через compose Redis доступен на `localhost:6379` с хоста.

## Структура БД

Таблица `images` (см. миграцию `migrations/versions/01_add_images_model.py`):
- `id` UUID PK
- `title` VARCHAR(32) UNIQUE NOT NULL
- `description` VARCHAR(32) NOT NULL
- `filename` VARCHAR(128) NOT NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT now()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT now()  
  (в ORM поле настроено с `onupdate=func.now()`)
- `file_url` VARCHAR(128) NOT NULL

SQL из миграции:
```sql
CREATE TABLE images (
  id UUID PRIMARY KEY,
  title VARCHAR(32) UNIQUE NOT NULL,
  description VARCHAR(32) NOT NULL,
  filename VARCHAR(128) NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  file_url VARCHAR(128) NOT NULL
);
```

## Полезные команды

- Применить миграции:
```bash
uv run alembic upgrade head
```
- Dev‑сервер с перезапуском:
```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Сборка Docker‑образа вручную:
```bash
docker build -t photo-gallery .
```
- Запуск только backend‑контейнера (нужны внешние db/redis):
```bash
docker run --rm -p 8000:8000 \
  -e DB_HOST=host.docker.internal -e DB_PORT=5432 \
  -e POSTGRES_DB=postgres -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres_password \
  -e REDIS_HOST=host.docker.internal -e REDIS_PORT=6379 \
  photo-gallery /app/docker_scripts/backend.sh
```

