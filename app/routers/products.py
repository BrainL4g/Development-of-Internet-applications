from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .. import schemas, services
from ..database import get_db

router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[schemas.ProductResponse])
async def read_products(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
) -> List[schemas.ProductResponse]:
    """
    Получить список продуктов.

    Args:
        skip (int): Количество пропускаемых записей (по умолчанию: 0)
        limit (int): Максимальное количество возвращаемых записей (по умолчанию: 100)
        db (AsyncSession): Сессия базы данных

    Returns:
        List[schemas.ProductResponse]: Список продуктов
    """
    service = services.ProductService(db)
    return await service.list(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=schemas.ProductResponse)
async def read_product(
        product_id: int,
        db: AsyncSession = Depends(get_db)
) -> schemas.ProductResponse:
    """
    Получить продукт по ID.

    Args:
        product_id (int): ID продукта
        db (AsyncSession): Сессия базы данных

    Returns:
        schemas.ProductResponse: Продукт

    Raises:
        HTTPException: Если продукт не найден (404)
    """
    service = services.ProductService(db)
    product = await service.get(product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product


@router.post("/", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
        product: schemas.ProductCreate,
        db: AsyncSession = Depends(get_db)
) -> schemas.ProductResponse:
    """
    Создать новый продукт.

    Args:
        product (schemas.ProductCreate): Данные для создания продукта
        db (AsyncSession): Сессия базы данных

    Returns:
        schemas.ProductResponse: Созданный продукт
    """
    service = services.ProductService(db)
    return await service.create(product)


@router.put("/{product_id}", response_model=schemas.ProductResponse)
async def update_product(
        product_id: int,
        product: schemas.ProductUpdate,
        db: AsyncSession = Depends(get_db)
) -> schemas.ProductResponse:
    """
    Обновить продукт по ID.

    Args:
        product_id (int): ID продукта
        product (schemas.ProductUpdate): Данные для обновления продукта
        db (AsyncSession): Сессия базы данных

    Returns:
        schemas.ProductResponse: Обновленный продукт

    Raises:
        HTTPException: Если продукт не найден (404)
    """
    service = services.ProductService(db)
    updated = await service.update(product_id, product)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return updated


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
        product_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Удалить продукт по ID.

    Args:
        product_id (int): ID продукта
        db (AsyncSession): Сессия базы данных

    Raises:
        HTTPException: Если продукт не найден (404)
    """
    service = services.ProductService(db)
    if not await service.delete(product_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
