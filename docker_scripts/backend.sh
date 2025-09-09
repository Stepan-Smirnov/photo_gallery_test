#!/bin/bash

uv run alembic upgrade head

uv run gunicorn app.main:app --worker-class uvicorn.workers.UvicornWorker --bind=0:8000