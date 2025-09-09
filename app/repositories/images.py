from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.images import Image
from app.repositories.base import BaseRepository


class ImagesRepository(BaseRepository[Image]):
    """Images repository"""

    def __init__(self, session: AsyncSession):
        super().__init__(session, Image)

    async def check_image_exists(self, title: str) -> Image | None:
        """Check if image exists"""

        return await self.session.scalar(select(Image).filter_by(title=title))
