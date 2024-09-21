from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.config import settings
from core.models import Base

engine = create_async_engine(
    url=settings.db.url,
    echo=True
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def session_getter():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def close_db_connection():
    await engine.dispose()

async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def delete_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)