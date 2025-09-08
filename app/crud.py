# app/crud.py
"""
CRUD operations for products.
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import List, Optional

from . import models, schemas


def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[models.Product]:
    """Retrieve a list of products with pagination."""
    return db.query(models.Product).offset(skip).limit(limit).all()


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Retrieve a single product by ID."""
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product."""
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(
    db: Session, product_id: int, product: schemas.ProductUpdate
) -> Optional[models.Product]:
    """Update an existing product."""
    db_product = get_product(db, product_id)
    if not db_product:
        return None
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """Delete a product by ID."""
    db_product = get_product(db, product_id)
    if not db_product:
        return False
    db.delete(db_product)
    db.commit()
    return True