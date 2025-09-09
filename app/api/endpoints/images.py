from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.depends import get_redis, get_session
from app.schemes.images import ImageCreate, ImageResponse, ImageUpdate
from app.use_cases.images import img_use_case

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
    session: Annotated[AsyncSession, Depends(get_session)],
    redis: Annotated[Redis, Depends(get_redis)],
):
    """
    - **title**: str - min 1, max 32 characters
    - **description**: str - min 1, max 32 characters
    - **file**: UploadFile - max 10MB
    """

    return await img_use_case.create_image(
        dto=image, file=file, redis=redis, session=session
    )


@router.get(
    path="/{id}",
    summary="Get image",
    response_model=ImageResponse,
    status_code=status.HTTP_200_OK,
)
async def get_image(
    id: str,
    redis: Annotated[Redis, Depends(get_redis)],
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """
    - **image_id**: str - image id
    """

    return await img_use_case.get_image(id=id, redis=redis, session=session)


@router.get(
    path="/",
    summary="Get all images",
    response_model=list[ImageResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_images(
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await img_use_case.get_all_images(session=session)


@router.patch(
    path="/{id}",
    summary="Update image",
    response_model=ImageResponse,
    status_code=status.HTTP_200_OK,
)
async def update_image(
    id: str,
    image: ImageUpdate,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    """
    - **image_id**: str - image id
    - **title**: str - min 1, max 32 characters
    - **description**: str - min 1, max 32 characters
    """

    return await img_use_case.update_image(id=id, session=session, image=image)


@router.delete(
    path="/{id}",
    summary="Delete image",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_image(
    id: str,
    session: Annotated[AsyncSession, Depends(get_session)],
):
    return await img_use_case.delete_image(id=id, session=session)
