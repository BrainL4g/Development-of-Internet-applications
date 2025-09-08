# app/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import AsyncGenerator

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./shop.db")

# Асинхронный движок для основного приложения
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

AsyncSessionLocal = async_sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine
)

# Синхронный движок для тестов
sync_engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)

SyncSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=sync_engine
)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()