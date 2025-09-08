from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core import settings

Base = declarative_base()

engine = create_async_engine(
    url=settings.database_url, pool_size=50, max_overflow=150
)
async_session = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)
