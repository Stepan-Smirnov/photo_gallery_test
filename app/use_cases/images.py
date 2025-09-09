import json
import logging
import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from redis.asyncio import Redis
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.constants import (
    IMAGE_EXTENSIONS,
    MAX_IMAGE_SIZE,
    ONE_CHUNK,
    REDIS_CHANNEL,
    REDIS_KEY_EXPIRE,
    REDIS_KEY_PREFIX,
)
from app.exception import (
    ImageAlreadyExists,
    ImageInvalidExtension,
    ImageTooLarge,
    ServerError,
)
from app.models.images import Image
from app.repositories.images import ImagesRepository
from app.schemes.images import (
    ImageCreate,
    ImageResponse,
    ImageUpdate,
    ImageWrite,
)

logger = logging.getLogger(__name__)


class ImageUseCase:
    """Image use case"""

    def __init__(self):
        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(parents=True, exist_ok=True)

    def _delete_file(self, file_url: Path) -> None:
        """Delete file in uploads directory"""

        if file_url.exists():
            file_url.unlink()

    async def create_image(
        self,
        session: AsyncSession,
        dto: ImageCreate,
        file: UploadFile,
        redis: Redis,
    ) -> Image:
        """Create image case"""

        if file.size > MAX_IMAGE_SIZE:
            raise ImageTooLarge

        if file.content_type not in IMAGE_EXTENSIONS:
            raise ImageInvalidExtension

        try:
            filename = file.filename
            file_url = (
                self.uploads_dir / f"{uuid.uuid4()}.{filename.split('.')[-1]}"
            )

            async with aiofiles.open(file_url, "wb") as f:
                while chunk := await file.read(ONE_CHUNK):
                    await f.write(chunk)

            dto = ImageWrite(
                title=dto.title,
                description=dto.description,
                filename=filename,
                file_url=str(file_url),
            )

            async with session.begin():
                img = await ImagesRepository(session=session).create(
                    instance=dto
                )

        except IntegrityError:
            self._delete_file(file_url=file_url)
            raise ImageAlreadyExists
        except Exception:
            self._delete_file(file_url=file_url)
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

        redis_key = f"{REDIS_KEY_PREFIX}{id}"
        try:
            img = await redis.get(name=redis_key)
            if img:
                return ImageResponse.model_validate_json(img)
        except Exception:
            logger.exception("Error getting image from redis")

        img = await ImagesRepository(session=session).get(id=id)

        try:
            await redis.set(
                name=redis_key,
                value=ImageResponse.model_validate(img).model_dump_json(),
                ex=REDIS_KEY_EXPIRE,
            )
        except Exception:
            logger.exception("Error setting image to redis")
        return img

    async def get_all_images(
        self,
        session: AsyncSession,
    ) -> list[Image]:
        """Get all images case"""

        return await ImagesRepository(session=session).get_list()

    async def update_image(
        self,
        session: AsyncSession,
        id: str,
        image: ImageUpdate,
    ) -> Image:
        """Update image case"""

        async with session.begin():
            img_repo = ImagesRepository(session=session)
            img = await img_repo.get(id=id)
            try:
                img = await img_repo.update(instance=img, data=image)
            except IntegrityError:
                raise ImageAlreadyExists
        return img

    async def delete_image(
        self,
        session: AsyncSession,
        id: str,
    ) -> None:
        """Delete image case"""

        async with session.begin():
            img_repo = ImagesRepository(session=session)
            img = await img_repo.get(id=id)
            await img_repo.delete(instance=img)
        self._delete_file(file_url=Path(img.file_url))


img_use_case = ImageUseCase()
