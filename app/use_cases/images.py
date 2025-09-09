import json
import logging
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from redis.asyncio import Redis

from app.constants import (
    IMAGE_EXTENSIONS,
    MAX_IMAGE_SIZE,
    ONE_CHUNK,
    REDIS_CHANNEL,
    REDIS_KEY_PREFIX,
    REDIS_KEY_EXPIRE,
)

from app.exception import (
    ImageAlreadyExists,
    ImageInvalidExtension,
    ImageTooLarge,
    ServerError,
)
from app.models.images import Image
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.images import ImagesRepository
from app.schemes.images import ImageCreate, ImageWrite, ImageResponse

logger = logging.getLogger(__name__)


class ImageUseCase:
    """Image use case"""

    def __init__(self):
        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(parents=True, exist_ok=True)

    async def create_image(
        self,
        session: AsyncSession,
        dto: ImageCreate,
        file: UploadFile,
        redis: Redis,
    ) -> Image:
        """Create image case"""

        img_repo: ImagesRepository = ImagesRepository(session=session)
        img = await img_repo.check_image_exists(title=dto.title)

        if img:
            raise ImageAlreadyExists
        if file.size > MAX_IMAGE_SIZE:
            raise ImageTooLarge

        if file.content_type not in IMAGE_EXTENSIONS:
            raise ImageInvalidExtension

        try:
            filename = file.filename
            file_url = self.uploads_dir / filename

            async with aiofiles.open(file_url, "wb") as f:
                while chunk := await file.read(ONE_CHUNK):
                    await f.write(chunk)

            dto = ImageWrite(
                title=dto.title,
                description=dto.description,
                filename=filename,
                file_url=str(file_url),
            )

            img = await img_repo.create(item=dto)
        except Exception:
            if file_url.exists():
                file_url.unlink()
            logger.exception(msg="Error uploading image")
            raise ServerError

        try:
            payload = dict(
                event="image_uploaded",
                id=str(img.id),
                title=img.title,
            )
            await redis.publish(REDIS_CHANNEL, json.dumps(payload))
        except Exception:
            logger.exception(msg="Error publishing image created event")
        return img

    async def get_image(
        self,
        session: AsyncSession,
        id: str,
        redis: Redis,
    ) -> Image:
        """Get image case"""

        img = await redis.get(name=f"{REDIS_KEY_PREFIX}{id}")
        if img:
            return ImageResponse.model_validate_json(img)


        img_repo: ImagesRepository = ImagesRepository(session=session)
        img = await img_repo.get(id=id)
    
        await redis.set(
                name=f"{REDIS_KEY_PREFIX}{id}",
                value=ImageResponse.model_validate(img).model_dump_json(),
                ex=REDIS_KEY_EXPIRE
            )
        return img

img_use_case = ImageUseCase()
