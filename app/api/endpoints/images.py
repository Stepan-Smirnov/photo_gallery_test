from typing import Annotated

from fastapi import Depends, File, UploadFile
from app.core.unit_of_work import UnitOfWork

from fastapi import APIRouter, status

from app.schemes.images import ImageCreate, ImageResponse
from app.api.depends import get_uow


router = APIRouter()


@router.post(
    path="/",
    summary="Create image",
    status_code=status.HTTP_201_CREATED,
)
async def create_image(
    image: Annotated[ImageCreate, Depends(ImageCreate)],
    file: Annotated[UploadFile, File(..., description="Image file")],
    uow: Annotated[UnitOfWork, Depends(get_uow)]
):
    """Create image"""
    pass