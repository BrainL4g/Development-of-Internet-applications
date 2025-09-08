# tests/test_products.py
"""
Unit and integration tests for products API.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from ..app import schemas, crud


@pytest.mark.parametrize("name,description,price", [
    ("Valid Product", "Desc", 100.0),
    ("", None, 50.0),  # Invalid: empty name
    ("Valid", "Desc", -10.0),  # Invalid: negative price
])
def test_create_product_valid(client: TestClient, db_session: Session, sample_product_data, name, description, price):
    """Test product creation (happy path)."""
    response = client.post(
        "/api/v1/products/",
        json={**sample_product_data, "name": name, "description": description, "price": price}
    )
    if name and price > 0:
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name
        assert data["price"] == price
        # Verify in DB
        db_product = crud.get_product(db_session, data["id"])
        assert db_product is not None
    else:
        assert response.status_code == 422  # Validation error


def test_get_products(client: TestClient, sample_product_data):
    """Test listing products."""
    # Create one
    client.post("/api/v1/products/", json=sample_product_data)
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1
    assert products[0]["name"] == sample_product_data["name"]


def test_get_product(client: TestClient, sample_product_data):
    """Test retrieving a single product."""
    create_resp = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_resp.json()["id"]
    response = client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == sample_product_data["name"]


def test_get_nonexistent_product(client: TestClient):
    """Test 404 for nonexistent product."""
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404


def test_update_product(client: TestClient, sample_product_data):
    """Test updating a product."""
    create_resp = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_resp.json()["id"]
    update_data = {"name": "Updated Laptop", "price": 1099.99}
    response = client.put(f"/api/v1/products/{product_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Laptop"
    assert data["price"] == 1099.99


def test_delete_product(client: TestClient, sample_product_data):
    """Test deleting a product."""
    create_resp = client.post("/api/v1/products/", json=sample_product_data)
    product_id = create_resp.json()["id"]
    response = client.delete(f"/api/v1/products/{product_id}")
    assert response.status_code == 204
    # Verify deletion
    get_resp = client.get(f"/api/v1/products/{product_id}")
    assert get_resp.status_code == 404


def test_delete_nonexistent_product(client: TestClient):
    """Test 404 on delete nonexistent."""
    response = client.delete("/api/v1/products/999")
    assert response.status_code == 404