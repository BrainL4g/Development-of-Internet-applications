# app/routers/products.py
"""
API router for products.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, services
from ..database import get_db

router = APIRouter()

product_service = services.ProductService  # For DI in future extensions


@router.get("/", response_model=List[schemas.ProductResponse])
def read_products(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    """Retrieve list of products (GET /api/v1/products)."""
    service = product_service(db)
    return service.list(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    """Retrieve a single product (GET /api/v1/products/{id})."""
    service = product_service(db)
    product = service.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    """Create a new product (POST /api/v1/products)."""
    service = product_service(db)
    return service.create(product)


@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)
):
    """Update a product (PUT /api/v1/products/{id})."""
    service = product_service(db)
    updated = service.update(product_id, product)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Delete a product (DELETE /api/v1/products/{id})."""
    service = product_service(db)
    if not service.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )