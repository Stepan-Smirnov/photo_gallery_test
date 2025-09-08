from datetime import datetime

from sqlalchemy import DateTime, String, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Image(Base):
    """Image model"""

    __tablename__ = "images"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    title: Mapped[str] = mapped_column(String(length=32), unique=True)
    description: Mapped[str] = mapped_column(String(length=32))
    filename: Mapped[str] = mapped_column(String(length=128))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
    file_url: Mapped[str] = mapped_column(String(length=128))

    def __repr__(self):
        return f"<Image {self.id} {self.title}>"
