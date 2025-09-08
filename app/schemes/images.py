from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


str_type = Annotated[str, Field(min_length=1, max_length=32)]

class ImageBase(BaseModel):
    """Image base scheme"""


    model_config = ConfigDict(
        extra="forbid", str_strip_whitespace=True
    )

class ImageCreate(ImageBase):
    """Image create scheme"""

    title: str_type
    description: str_type

class ImageUpdate(ImageBase):
    """Image update scheme"""

    title: str_type | None = None
    description: str_type | None = None



class ImageResponse(ImageBase):
    """Image response scheme"""

    id: int
    title: str_type
    description: str_type
    filename: str
    created_at: datetime
    updated_at: datetime
    file_url: str


