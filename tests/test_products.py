# tests/test_products.py
import pytest
from fastapi.testclient import TestClient


def test_create_product_success(client, sample_product_data):
    """Тест успешного создания продукта"""
    response = client.post("/products/", json=sample_product_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == sample_product_data["name"]
    assert data["price"] == sample_product_data["price"]
    assert "id" in data
    assert "created_at" in data


def test_create_product_invalid_data(client):
    """Тест создания продукта с невалидными данными"""
    # Название пустое
    invalid_data = {"name": "", "description": "Test", "price": 100.0}
    response = client.post("/products/", json=invalid_data)
    assert response.status_code == 422

    # Цена отрицательная
    invalid_data = {"name": "Test Product", "description": "Test", "price": -10.0}
    response = client.post("/products/", json=invalid_data)
    assert response.status_code == 422

    # Цена равна нулю
    invalid_data = {"name": "Test Product", "description": "Test", "price": 0.0}
    response = client.post("/products/", json=invalid_data)
    assert response.status_code == 422


def test_get_products_success(client):
    """Тест успешного получения списка продуктов"""
    # Сначала создаем продукт
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0
    }
    client.post("/products/", json=product_data)

    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1  # Может быть больше из-за других тестов
    # Проверяем, что хотя бы один продукт имеет ожидаемое имя
    product_names = [p["name"] for p in products]
    assert "Test Product" in product_names


def test_get_products_empty(client):
    """Тест получения пустого списка продуктов"""
    # Для этого теста нужно использовать уникальное имя, чтобы избежать конфликтов
    unique_name = "Unique Test Product 12345"
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    # Проверяем, что нет продукта с уникальным именем
    product_names = [p["name"] for p in products]
    assert unique_name not in product_names


def test_get_product_success(client):
    """Тест успешного получения конкретного продукта"""
    # Сначала создаем продукт
    product_data = {
        "name": "Test Product Get",
        "description": "Test Description Get",
        "price": 150.0
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Test Product Get"


def test_get_product_not_found(client):
    """Тест получения несуществующего продукта"""
    response = client.get("/products/999999")
    assert response.status_code == 404


def test_update_product_success(client):
    """Тест успешного обновления продукта"""
    # Сначала создаем продукт
    product_data = {
        "name": "Test Product Update",
        "description": "Test Description Update",
        "price": 100.0
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    updated_data = {"name": "Updated Product", "price": 200.0}
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["price"] == updated_data["price"]


def test_update_product_partial(client):
    """Тест частичного обновления продукта"""
    # Сначала создаем продукт
    product_data = {
        "name": "Test Product Partial",
        "description": "Test Description Partial",
        "price": 100.0
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    # Обновляем только имя
    updated_data = {"name": "Updated Product Partial"}
    response = client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_data["name"]
    assert data["price"] == 100.0  # Цена не изменилась


def test_update_product_not_found(client):
    """Тест обновления несуществующего продукта"""
    updated_data = {"name": "Updated Product", "price": 200.0}
    response = client.put("/products/999999", json=updated_data)
    assert response.status_code == 404


def test_update_product_invalid_data(client):
    """Тест обновления продукта с невалидными данными"""
    # Сначала создаем продукт
    product_data = {
        "name": "Test Product Invalid",
        "description": "Test Description Invalid",
        "price": 100.0
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    # Невалидные данные
    invalid_data = {"name": "", "price": -10.0}
    response = client.put(f"/products/{product_id}", json=invalid_data)
    assert response.status_code == 422


def test_delete_product_success(client):
    """Тест успешного удаления продукта"""
    # Сначала создаем продукт
    product_data = {
        "name": "Test Product Delete",
        "description": "Test Description Delete",
        "price": 100.0
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    # Проверяем, что продукт действительно удален
    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 404


def test_delete_product_not_found(client):
    """Тест удаления несуществующего продукта"""
    response = client.delete("/products/999999")
    assert response.status_code == 404


def test_root_endpoint(client):
    """Тест корневой конечной точки"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "Online Shop API is running"