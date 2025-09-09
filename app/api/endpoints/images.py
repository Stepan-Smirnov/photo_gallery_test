import logging

from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from redis.asyncio import Redis

from app.api.depends import get_uow, get_redis
from app.core.unit_of_work import UnitOfWork
from app.schemes.images import ImageCreate, ImageResponse
from app.use_cases.images import img_use_case
from app.exception import ServerError


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    path="/",
    summary="Create image",
    status_code=status.HTTP_201_CREATED,
    response_model=ImageResponse,
)
async def create_image(
    image: Annotated[ImageCreate, Depends()],
    file: Annotated[UploadFile, File(description="Image file")],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    """
    - *title**: str - min 1, max 32 characters
    - **description**: str - min 1, max 32 characters
    - **file**: UploadFile - max 10MB
    """
    
    try:
        return await img_use_case.create_image(
            uow=uow, dto=image, file=file, redis=redis
        )
    except Exception:
        logger.exception(msg="Error creating image")
        raise ServerError


