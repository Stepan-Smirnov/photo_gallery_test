from contextlib import asynccontextmanager

from fastapi import FastAPI
from redis.asyncio import Redis

from app.api.routers import main_router
from app.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan"""

    app.state.redis = Redis.from_url(
        settings.redis_url,
        decode_responses=True,
        encoding="utf-8",
    )
    await app.state.redis.ping()
    try:
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)
app.include_router(main_router)
