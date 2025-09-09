from collections.abc import AsyncGenerator

from fastapi import Request
from redis.asyncio import Redis

from app.core.db import async_session_maker
from app.core.unit_of_work import UnitOfWork


def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """Get unit of work"""

    return UnitOfWork(session_factory=async_session_maker)


def get_redis(request: Request) -> Redis:
    """Get redis"""
    return request.app.state.redis
