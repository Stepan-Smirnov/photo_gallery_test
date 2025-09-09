from collections.abc import AsyncGenerator

from fastapi import Request
from redis.asyncio import Redis

from app.core.db import async_session_maker
from sqlalchemy.ext.asyncio import AsyncSession

async def get_session() -> AsyncSession:
    """Get session"""

    async with async_session_maker() as async_session:
        try:
            yield async_session
        finally:
            await async_session.close()

def get_redis(request: Request) -> Redis:
    """Get redis"""

    return request.app.state.redis
