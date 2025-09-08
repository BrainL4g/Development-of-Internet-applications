"""
CRUD операции для модели Product.

Этот модуль содержит асинхронные CRUD (Create, Read, Update, Delete) операции
для модели Product с использованием асинхронного ORM SQLAlchemy.
"""

from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas

__all__ = [
    "get_products",
    "get_product",
    "create_product",
    "update_product",
    "delete_product"
]


async def get_products(
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
) -> List[models.Product]:
    """
    Получить список продуктов с пагинацией.

    Аргументы:
        db (AsyncSession): Сессия базы данных
        skip (int): Количество пропускаемых записей (смещение)
        limit (int): Максимальное количество возвращаемых записей

    Возвращает:
        List[models.Product]: Список объектов Product
    """
    stmt = select(models.Product).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_product(
        db: AsyncSession,
        product_id: int
) -> Optional[models.Product]:
    """
    Получить один продукт по ID.

    Аргументы:
        db (AsyncSession): Сессия базы данных
        product_id (int): ID продукта для получения

    Возвращает:
        Optional[models.Product]: Объект Product если найден, иначе None
    """
    stmt = select(models.Product).where(models.Product.id == product_id)
    result = await db.execute(stmt)
    return result.scalars().first()


async def create_product(
        db: AsyncSession,
        product: schemas.ProductCreate
) -> models.Product:
    """
    Создать новый продукт.

    Аргументы:
        db (AsyncSession): Сессия базы данных
        product (schemas.ProductCreate): Данные для создания продукта

    Возвращает:
        models.Product: Созданный объект Product
    """
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(
        db: AsyncSession,
        product_id: int,
        product: schemas.ProductUpdate
) -> Optional[models.Product]:
    """
    Обновить существующий продукт.

    Аргументы:
        db (AsyncSession): Сессия базы данных
        product_id (int): ID продукта для обновления
        product (schemas.ProductUpdate): Данные для обновления продукта

    Возвращает:
        Optional[models.Product]: Обновленный объект Product если найден, иначе None
    """
    db_product = await get_product(db, product_id)
    if not db_product:
        return None

    update_data = product.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)

    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(
        db: AsyncSession,
        product_id: int
) -> bool:
    """
    Удалить продукт по ID.

    Аргументы:
        db (AsyncSession): Сессия базы данных
        product_id (int): ID продукта для удаления

    Возвращает:
        bool: True если продукт был удален, False если не найден
    """
    db_product = await get_product(db, product_id)
    if not db_product:
        return False

    await db.delete(db_product)
    await db.commit()
    return True
