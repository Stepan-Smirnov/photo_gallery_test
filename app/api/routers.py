from fastapi import APIRouter

from app.api.endpoints import images_router


main_router = APIRouter(prefix="/api/v1")

main_router.include_router(
    router=images_router,
    prefix="/images",
    tags=["images"],
)
