# app/services.py
"""
Business services for product operations (extensible layer).
"""
import logging
from typing import Optional

from sqlalchemy.orm import Session
from . import crud, schemas

logger = logging.getLogger(__name__)


class ProductService:
    """Service class for product-related operations."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, product_in: schemas.ProductCreate) -> schemas.ProductResponse:
        """Create a product with logging."""
        logger.info(f"Creating product: {product_in.name}")
        return schemas.ProductResponse.from_orm(crud.create_product(self.db, product_in))

    def get(self, product_id: int) -> Optional[schemas.ProductResponse]:
        """Get a product with validation."""
        product = crud.get_product(self.db, product_id)
        if not product:
            logger.warning(f"Product {product_id} not found")
            return None
        return schemas.ProductResponse.from_orm(product)

    def list(self, skip: int = 0, limit: int = 100) -> list[schemas.ProductResponse]:
        """List products."""
        products = crud.get_products(self.db, skip=skip, limit=limit)
        return [schemas.ProductResponse.from_orm(p) for p in products]

    def update(self, product_id: int, product_in: schemas.ProductUpdate) -> Optional[schemas.ProductResponse]:
        """Update a product."""
        product = crud.update_product(self.db, product_id, product_in)
        if not product:
            logger.warning(f"Failed to update product {product_id}")
            return None
        return schemas.ProductResponse.from_orm(product)

    def delete(self, product_id: int) -> bool:
        """Delete a product."""
        success = crud.delete_product(self.db, product_id)
        if success:
            logger.info(f"Deleted product {product_id}")
        else:
            logger.warning(f"Product {product_id} not found for deletion")
        return success