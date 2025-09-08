from typing import AsyncGenerator

from app.core.unit_of_work import UnitOfWork
from app.core.db import async_session_maker



async def get_uow() -> AsyncGenerator:
    """Get unit of work"""
    async with UnitOfWork(session_factory=async_session_maker) as uow:
        yield uow