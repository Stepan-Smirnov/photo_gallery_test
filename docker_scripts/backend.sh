#!/bin/bash

uv run alembic upgrade head

uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000