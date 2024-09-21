import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from core.database import session_getter
from core.main import app
from core.models import Base

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/notes",
    echo=True
)
AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

async def override_session_getter():
    async with AsyncSessionLocal() as session:
            yield session

app.dependency_overrides[session_getter] = override_session_getter

@pytest.fixture(scope='session', autouse=True)
async def setup_and_teardown_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

