import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from typing import AsyncGenerator

from ..app.database import Base, get_db
from ..app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test_shop.db"
engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope="module")
async def client(db_session: AsyncSession) -> TestClient:
    async def override_get_db():
        try:
            yield db_session
        finally:
            await db_session.close()

    app.dependency_overrides[get_db]