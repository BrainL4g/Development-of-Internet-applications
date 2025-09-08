"""
Сервисный слой для работы с продуктами.

Этот модуль содержит бизнес-логику для операций с продуктами,
включая создание, получение, обновление и удаление.
"""

import logging
from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from . import crud, schemas

logger = logging.getLogger(__name__)

__all__ = ["ProductService"]


class ProductService:
    """
    Сервис для работы с продуктами.

    Предоставляет методы для CRUD операций с продуктами,
    используя слой доступа к данным (crud) и сессию базы данных.
    """

    def __init__(self, db: AsyncSession):
        """
        Инициализация сервиса продуктами.

        Аргументы:
            db (AsyncSession): Асинхронная сессия базы данных
        """
        self.db = db

    async def create(self, product_in: schemas.ProductCreate) -> schemas.ProductResponse:
        """
        Создать новый продукт.

        Аргументы:
            product_in (schemas.ProductCreate): Данные для создания продукта

        Возвращает:
            schemas.ProductResponse: Созданный продукт

        Логирование:
            INFO: Записывает информацию о создании продукта
        """
        logger.info(f"Creating product: {product_in.name}")
        product = await crud.create_product(self.db, product_in)
        return schemas.ProductResponse.model_validate(product)

    async def get(self, product_id: int) -> Optional[schemas.ProductResponse]:
        """
        Получить продукт по ID.

        Аргументы:
            product_id (int): ID продукта для получения

        Возвращает:
            Optional[schemas.ProductResponse]: Продукт если найден, иначе None

        Логирование:
            WARNING: Записывает предупреждение если продукт не найден
        """
        product = await crud.get_product(self.db, product_id)
        if not product:
            logger.warning(f"Product {product_id} not found")
            return None
        return schemas.ProductResponse.model_validate(product)

    async def list(self, skip: int = 0, limit: int = 100) -> List[schemas.ProductResponse]:
        """
        Получить список продуктов с пагинацией.

        Аргументы:
            skip (int): Количество пропускаемых записей (по умолчанию: 0)
            limit (int): Максимальное количество возвращаемых записей (по умолчанию: 100)

        Возвращает:
            List[schemas.ProductResponse]: Список продуктов
        """
        products = await crud.get_products(self.db, skip=skip, limit=limit)
        return [schemas.ProductResponse.model_validate(p) for p in products]

    async def update(self, product_id: int, product_in: schemas.ProductUpdate) -> Optional[schemas.ProductResponse]:
        """
        Обновить существующий продукт.

        Аргументы:
            product_id (int): ID продукта для обновления
            product_in (schemas.ProductUpdate): Данные для обновления продукта

        Возвращает:
            Optional[schemas.ProductResponse]: Обновленный продукт если найден, иначе None

        Логирование:
            WARNING: Записывает предупреждение если продукт не найден для обновления
        """
        product = await crud.update_product(self.db, product_id, product_in)
        if not product:
            logger.warning(f"Failed to update product {product_id}")
            return None
        return schemas.ProductResponse.model_validate(product)

    async def delete(self, product_id: int) -> bool:
        """
        Удалить продукт по ID.

        Аргументы:
            product_id (int): ID продукта для удаления

        Возвращает:
            bool: True если продукт был удален, False если не найден

        Логирование:
            INFO: Записывает информацию об успешном удалении продукта
            WARNING: Записывает предупреждение если продукт не найден для удаления
        """
        success = await crud.delete_product(self.db, product_id)
        if success:
            logger.info(f"Deleted product {product_id}")
        else:
            logger.warning(f"Product {product_id} not found for deletion")
        return success