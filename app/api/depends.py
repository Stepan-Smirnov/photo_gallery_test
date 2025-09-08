from collections.abc import AsyncGenerator

from app.core.db import async_session_maker
from app.core.unit_of_work import UnitOfWork


async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """Get unit of work"""

    async with UnitOfWork(session_factory=async_session_maker) as uow:
        yield uow
        