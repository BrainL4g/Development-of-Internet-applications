import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from ..app import schemas, crud

@pytest.mark.asyncio
@pytest.mark.parametrize("name,description,price", [
    ("Valid Product", "Desc", 100.0),
    ("", None, 50.0),
    ("Valid", "Desc", -10.0),
])
async def test_create_product_valid(client: TestClient, db_session: AsyncSession, sample_product_data: dict[str, str | float], name: str, description: str | None, price: float) -> None:
    response = client.post(
        "/products/",
        json={**sample_product_data, "name": name, "description": description, "price": price}
    )
    if name and price > 0:
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == name
        assert data["price"] == price
        db_product = await crud.get_product(db_session, data["id"])
        assert db_product is not None
    else:
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_get_products(client: TestClient, sample_product_data: dict[str, str | float]) -> None:
    client.post("/products/", json=sample_product_data)
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert len(products) >= 1
    assert products[0]["name"] == sample_product_data["name"]