FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:0.6.8 /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
RUN chmod a+x docker_scripts/*.sh