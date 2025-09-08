from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from . import models, schemas


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Product]:
    result = await db.execute(
        models.Product.__table__.select().offset(skip).limit(limit)
    )
    return result.scalars().all()


async def get_product(db: AsyncSession, product_id: int) -> Optional[models.Product]:
    result = await db.execute(
        models.Product.__table__.select().where(models.Product.id == product_id)
    )
    return result.scalars().first()


async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(
        db: AsyncSession, product_id: int, product: schemas.ProductUpdate
) -> Optional[models.Product]:
    db_product = await get_product(db, product_id)
    if not db_product:
        return None
    update_data = product.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int) -> bool:
    db_product = await get_product(db, product_id)
    if not db_product:
        return False
    await db.delete(db_product)
    await db.commit()
    return True
