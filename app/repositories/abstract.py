from abc import ABC, abstractmethod


class AbstractRepository[T](ABC):
    """Abstract repository class"""

    @abstractmethod
    async def add(self, item: T) -> T: ...

    @abstractmethod
    async def get(self, id: str) -> T | None: ...

    @abstractmethod
    async def get_list(self) -> list[T]: ...

    @abstractmethod
    async def update(self, item: T) -> T: ...

    @abstractmethod
    async def delete(self, id: str) -> None: ...
