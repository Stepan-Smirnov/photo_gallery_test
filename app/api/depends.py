from collections.abc import AsyncGenerator

from app.core.db import async_session_maker
from app.core.unit_of_work import UnitOfWork


def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    """Get unit of work"""

    return UnitOfWork(session_factory=async_session_maker)
        