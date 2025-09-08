from typing import Annotated

<<<<<<< HEAD
from fastapi import APIRouter, Depends, File, UploadFile, status
=======
from fastapi import Depends, File, UploadFile
from app.core.unit_of_work import UnitOfWork
>>>>>>> 0cbf81f30e3afd6b32d741d47486a38b1054a65c

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
    image: Annotated[ImageCreate, Depends(ImageCreate)],
    file: Annotated[UploadFile, File(..., description="Image file")],
<<<<<<< HEAD
    uow: Annotated[UnitOfWork, Depends(get_uow)],
):
    """Create image"""
    pass
=======
    uow: Annotated[UnitOfWork, Depends(get_uow)]
):
    """Create image"""
    pass
>>>>>>> 0cbf81f30e3afd6b32d741d47486a38b1054a65c
