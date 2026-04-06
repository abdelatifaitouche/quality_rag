from src.core.db.engine import engine
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


AsyncSessionLocal = async_sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)
