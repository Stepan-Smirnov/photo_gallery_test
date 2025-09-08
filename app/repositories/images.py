from sqlalchemy.ext.asyncio import AsyncSession

from app.models.images import Image
from app.repositories.base import BaseRepository


class ImagesRepository(BaseRepository[Image]):
    """Images repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Image)
