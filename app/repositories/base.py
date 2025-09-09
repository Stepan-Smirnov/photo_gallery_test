from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import ObjNotFound
from app.repositories.abstract import AbstractRepository


class BaseRepository[T](AbstractRepository[T]):
    """Base repository class"""

    def __init__(self, session: AsyncSession, model: T) -> None:
        self.session = session
        self.model = model

    async def create(self, instance: BaseModel) -> T:
        """Add item to database"""

        instance = self.model(**instance.model_dump())
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def get(self, id: str | int) -> T:
        """Get item from database or none"""

        result = await self.session.scalar(select(self.model).filter_by(id=id))
        if not result:
            raise ObjNotFound
        return result

    async def get_list(self, **params) -> list[T]:
        """Get list of items from database"""

        result = await self.session.scalars(
            select(self.model).filter_by(**params)
        )
        return result.all()

    async def update(self, instance: T, data: BaseModel) -> T:
        """Update item in database"""

        data = data.model_dump(exclude_unset=True)
        for attr, value in data.items():
            setattr(instance, attr, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: T) -> None:
        """Delete item from database"""

        await self.session.delete(instance)
