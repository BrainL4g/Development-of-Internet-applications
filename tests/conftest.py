# tests/conftest.py
"""
Pytest fixtures for testing.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from ..app.database import Base, get_db
from ..app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test_shop.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh DB session per test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client(db_session):
    """Override get_db dependency for tests."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_product_data():
    """Sample product data for tests."""
    return {
        "name": "Test Laptop",
        "description": "A powerful laptop",
        "price": 999.99
    }