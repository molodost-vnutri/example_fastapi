from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from src.config import settings

engine = create_async_engine(url=settings.DATABASE_URL)

async_session_maker = async_sessionmaker(bind=engine, class_=AsyncSession)

class Base(DeclarativeBase):
    pass