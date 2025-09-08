import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, product_in: schemas.ProductCreate) -> schemas.ProductResponse:
        logger.info(f"Creating product: {product_in.name}")
        # Исправлено: используем model_validate вместо from_orm
        product = await crud.create_product(self.db, product_in)
        return schemas.ProductResponse.model_validate(product)

    async def get(self, product_id: int) -> Optional[schemas.ProductResponse]:
        product = await crud.get_product(self.db, product_id)
        if not product:
            logger.warning(f"Product {product_id} not found")
            return None
        # Исправлено: используем model_validate вместо from_orm
        return schemas.ProductResponse.model_validate(product)

    async def list(self, skip: int = 0, limit: int = 100) -> list[schemas.ProductResponse]:
        products = await crud.get_products(self.db, skip=skip, limit=limit)
        # Исправлено: используем model_validate вместо from_orm
        return [schemas.ProductResponse.model_validate(p) for p in products]

    async def update(self, product_id: int, product_in: schemas.ProductUpdate) -> Optional[schemas.ProductResponse]:
        product = await crud.update_product(self.db, product_id, product_in)
        if not product:
            logger.warning(f"Failed to update product {product_id}")
            return None
        # Исправлено: используем model_validate вместо from_orm
        return schemas.ProductResponse.model_validate(product)

    async def delete(self, product_id: int) -> bool:
        success = await crud.delete_product(self.db, product_id)
        if success:
            logger.info(f"Deleted product {product_id}")
        else:
            logger.warning(f"Product {product_id} not found for deletion")
        return success