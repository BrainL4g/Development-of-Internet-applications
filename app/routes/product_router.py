from fastapi import APIRouter, status
from typing import Annotated
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.deps import ProductServiceDep

router = APIRouter(prefix="/products", tags=["Products"])  # Вернули оригинальный префикс

@router.get("/", response_model=list[ProductRead])
async def list_products(service: ProductServiceDep):
    return await service.list_products()

@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, service: ProductServiceDep):
    return await service.get_product(product_id)

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, service: ProductServiceDep):
    return await service.create_product(payload)

@router.put("/{product_id}", response_model=ProductRead)
async def update_product(product_id: int, payload: ProductUpdate, service: ProductServiceDep):
    return await service.update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, service: ProductServiceDep):
    await service.delete_product(product_id)