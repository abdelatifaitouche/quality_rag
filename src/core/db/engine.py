from sqlalchemy.ext.asyncio import create_async_engine
import os


DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE URL IS MISSING")


engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)
