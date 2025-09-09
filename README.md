# Photo Gallery (FastAPI)

Сервис на FastAPI для загрузки изображений. Хранение — Postgres, кеш и события — Redis.

## Запуск (Docker)

Требования: Docker, Docker Compose.

1) Создайте .env из примера:
```bash
cp env.docker.example .env       # Linux/macOS
# или PowerShell:
copy env.docker.example .env
```
2) Запустите сервисы:
```bash
docker compose up --build
```
3) Откройте документацию:
- Swagger UI: http://localhost:8000/docs

## Минимальные примеры API (curl)

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

## Структура БД

Таблица `images`:
- `id` UUID PK
- `title` VARCHAR(32) UNIQUE NOT NULL
- `description` VARCHAR(32) NOT NULL
- `filename` VARCHAR(128) NOT NULL
- `created_at` TIMESTAMPTZ NOT NULL DEFAULT now()
- `updated_at` TIMESTAMPTZ NOT NULL DEFAULT now()
- `file_url` VARCHAR(128) NOT NULL

