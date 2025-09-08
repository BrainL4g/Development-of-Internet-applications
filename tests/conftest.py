"""
Фикстуры для тестирования приложения.

Этот файл содержит общие фикстуры, которые используются в тестах,
включая настройку тестовой базы данных и клиент для API.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.database import Base

__all__ = ["sample_product_data", "client"]

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def sample_product_data() -> dict[str, str | float]:
    """
    Фикстура с тестовыми данными для продукта.

    Возвращает:
        dict[str, str | float]: Словарь с данными тестового продукта
    """
    return {
        "name": "Test Laptop",
        "description": "A powerful laptop",
        "price": 999.99
    }


@pytest.fixture(scope="function")
def client() -> TestClient:
    """
    Фикстура для тестового клиента FastAPI.

    Создает изолированную среду для каждого теста с отдельной
    тестовой базой данных, которая очищается после теста.

    Возвращает:
        TestClient: Клиент для тестирования API
    """
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)
