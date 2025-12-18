from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_db
from services.product_service import ProductService
from repositories.product_repository import ProductRepository
from schemas.product import (
    ProductCreateForm, ProductUpdate, ProductResponse, ProductCreate
)
from typing import List

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
async def get_products(db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return await service.get_all()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return await service.get_by_id(product_id)

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    name: str = Form(...),
    description: str | None = Form(None),
    price: float = Form(..., gt=0),
    stock: int = Form(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    service = ProductService(repo)
    create_data = ProductCreate(name=name, description=description, price=price, stock=stock)
    return await service.create(create_data)

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    db: AsyncSession = Depends(get_db)
):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return await service.update(product_id, product)

@router.delete("/{product_id}")
async def delete_product(product_id: int, db: AsyncSession = Depends(get_db)):
    repo = ProductRepository(db)
    service = ProductService(repo)
    return await service.delete(product_id)