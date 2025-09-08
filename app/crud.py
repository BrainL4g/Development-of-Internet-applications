from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from sqlalchemy import select

from . import models, schemas

async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.Product]:
    # Исправлено: используем select правильно
    stmt = select(models.Product).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())

async def get_product(db: AsyncSession, product_id: int) -> Optional[models.Product]:
    # Исправлено: используем select правильно
    stmt = select(models.Product).where(models.Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> models.Product:
    # Исправлено: используем model_dump вместо dict()
    db_product = models.Product(**product.model_dump())
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
    # Исправлено: используем model_dump вместо dict()
    update_data = product.model_dump(exclude_unset=True)
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