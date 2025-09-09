from abc import ABC, abstractmethod

from pydantic import BaseModel


class AbstractRepository[T](ABC):
    """Abstract repository class"""

    @abstractmethod
    async def create(self, instance: BaseModel) -> T: ...

    @abstractmethod
    async def get(self, id: str | int) -> T | None: ...

    @abstractmethod
    async def get_list(self) -> list[T]: ...

    @abstractmethod
    async def update(self, instance: T, data: BaseModel) -> T: ...

    @abstractmethod
    async def delete(self, instance: T) -> None: ...
