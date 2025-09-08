from redis.asyncio import Redis
from fastapi import FastAPI
from contextlib import asynccontextmanager

from starlette.background import P

from app.core import settings

@asynccontextmanager
async def lifespan(app: FastAPI):

    app.state.redis = Redis.from_url(
        settings.redis_url, decode_responses=True, encoding="utf-8",
         password=settings.REDIS_PASSWORD
    )
    await app.state.redis.aclose()
    try:
        yield
    finally:
        await app.state.redis.aclose()


app = FastAPI(lifespan=lifespan)
