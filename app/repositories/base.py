from pydantic import BaseModel
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.exception import ObjNotFound
from app.repositories.abstract import AbstractRepository


class BaseRepository[T](AbstractRepository[T]):
    """Base repository class"""

    def __init__(self, session: AsyncSession, model: T) -> None:
        self.session = session
        self.model = model

    async def create(self, item: BaseModel) -> T:
        """Add item to database"""

        obj = self.model(**item.model_dump())
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get(self, id: str | int) -> T | None:
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

    async def update(self, obj: T, obj_data: BaseModel) -> T:
        """Update item in database"""

        update_data = obj_data.model_dump(exclude_unset=True)
        query = (
            update(self.model)
            .where(self.model.id == obj.id)
            .values(**update_data)
        )
        await self.session.execute(query)
        return obj

    async def delete(self, obj: T) -> None:
        """Delete item from database"""

        await self.session.delete(obj)
