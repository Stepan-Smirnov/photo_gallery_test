from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile, status
from app.core.unit_of_work import UnitOfWork

from app.api.depends import get_uow
from app.core.unit_of_work import UnitOfWork
from app.schemes.images import ImageCreate

router = APIRouter()


@router.post(
    path="/",
    summary="Create image",
    status_code=status.HTTP_201_CREATED,
)
async def create_image(
    image: Annotated[ImageCreate, Depends()],
    file: Annotated[UploadFile, File(description="Image file")],
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Create image"""
    pass
