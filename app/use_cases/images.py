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
)
from app.core.unit_of_work import UnitOfWork
from app.exception import (
    ImageAlreadyExists,
    ImageInvalidExtension,
    ImageTooLarge,
    ServerError,
)
from app.models.images import Image
from app.repositories.images import ImagesRepository
from app.schemes.images import ImageCreate, ImageWrite

logger = logging.getLogger(__name__)


class ImageUseCase:
    """Image use case"""

    def __init__(self):
        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(parents=True, exist_ok=True)

    async def create_image(
        self,
        uow: UnitOfWork,
        dto: ImageCreate,
        file: UploadFile,
        redis: Redis,
    ) -> Image:
        """Create image case"""

        async with uow:
            img_repo: ImagesRepository = uow.repo(ImagesRepository)
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


img_use_case = ImageUseCase()
