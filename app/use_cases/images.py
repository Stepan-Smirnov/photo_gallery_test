from pathlib import Path

import aiofiles
from fastapi import UploadFile

from app.constants import IMAGE_EXTENSIONS, MAX_IMAGE_SIZE
from app.core.unit_of_work import UnitOfWork
from app.exception import (
    ImageAlreadyExists,
    ImageInvalidExtension,
    ImageTooLarge,
)
from app.models.images import Image
from app.repositories.images import ImagesRepository
from app.schemes.images import ImageCreate, ImageWrite


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
    ) -> Image:
        """Create image case"""
        
        img_repo = uow.repo(ImagesRepository)
        img = await img_repo.check_image_exists(dto.title)
        if img:
            raise ImageAlreadyExists
        if file.size > MAX_IMAGE_SIZE:
            raise ImageTooLarge

        if file.content_type not in IMAGE_EXTENSIONS:
            raise ImageInvalidExtension

        filename = file.filename
        file_url = self.uploads_dir / filename

        async with aiofiles.open(file_url, "wb") as f:
            await f.write(file.file.read())

        dto = ImageWrite(
            title=dto.title,
            description=dto.description,
            filename=filename,
            file_url=str(file_url),
        )

        img = await img_repo.add(item=dto)
        return img


img_use_case = ImageUseCase()