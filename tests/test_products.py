import pytest
from httpx import AsyncClient, ASGITransport
from unittest.mock import AsyncMock
from app.main import app
from app.deps import get_product_service

@pytest.fixture
def mock_service():
    return AsyncMock()

@pytest.fixture(autouse=True)
def override_dependency(mock_service):
    app.dependency_overrides[get_product_service] = lambda: mock_service
    yield
    app.dependency_overrides.clear()

@pytest.mark.asyncio
async def test_list_products(mock_service):
    """
    Тест: получение списка всех продуктов (GET /products/).
    Проверяет, что эндпоинт возвращает корректный список продуктов.
    """
    mock_service.list_products.return_value = [
        {"id": 1, "title": "Laptop", "description": "Gaming", "price": 1000.0, "sku": "ABC123"}
    ]
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/products/")
    assert r.status_code == 200
    assert r.json()[0]["title"] == "Laptop"

@pytest.mark.asyncio
async def test_get_product(mock_service):
    """
    Тест: получение конкретного продукта по ID (GET /products/{id}).
    Проверяет, что эндпоинт возвращает корректные данные продукта.
    """
    mock_service.get_product.return_value = {
        "id": 1, "title": "Phone", "description": "Android", "price": 500.0, "sku": "XYZ789"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.get("/products/1")
    assert r.status_code == 200
    assert r.json()["sku"] == "XYZ789"

@pytest.mark.asyncio
async def test_create_product(mock_service):
    """
    Тест: создание нового продукта (POST /products/).
    Проверяет, что эндпоинт создает продукт и возвращает его с присвоенным ID.
    """
    mock_service.create_product.return_value = {
        "id": 2, "title": "Tablet", "description": "iPad", "price": 700.0, "sku": "TBL999"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.post("/products/", json={"title": "Tablet", "description": "iPad", "price": 700.0, "sku": "TBL999"})
    assert r.status_code == 201
    assert r.json()["sku"] == "TBL999"

@pytest.mark.asyncio
async def test_update_product(mock_service):
    """
    Тест: обновление продукта (PUT /products/{id}).
    Проверяет, что эндпоинт обновляет данные продукта и возвращает обновленную версию.
    """
    mock_service.update_product.return_value = {
        "id": 2, "title": "Tablet Pro", "description": "iPad Pro", "price": 900.0, "sku": "TBL999"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.put("/products/2", json={"title": "Tablet Pro", "price": 900.0})
    assert r.status_code == 200
    assert r.json()["title"] == "Tablet Pro"

@pytest.mark.asyncio
async def test_delete_product(mock_service):
    """
    Тест: удаление продукта (DELETE /products/{id}).
    Проверяет, что эндпоинт удаляет продукт и возвращает статус 204 без содержимого.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        r = await ac.delete("/products/2")
    assert r.status_code == 204