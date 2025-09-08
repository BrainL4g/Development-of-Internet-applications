# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.main import app
from app.database import Base

# Используем синхронную базу данных для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def sample_product_data():
    return {
        "name": "Test Laptop",
        "description": "A powerful laptop",
        "price": 999.99
    }

@pytest.fixture
def client():
    # Создаем новую базу данных для каждого теста
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)