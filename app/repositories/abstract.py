from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractRepository[T](ABC):
    """Abstract repository class"""

    @abstractmethod
    async def create(self, item: BaseModel) -> T: ...

    @abstractmethod
    async def get(self, id: str | int) -> T | None: ...

    @abstractmethod
    async def get_list(self) -> list[T]: ...

    @abstractmethod
    async def update(self, item: T, obj_data: BaseModel) -> T: ...

    @abstractmethod
    async def delete(self, id: str) -> None: ...
