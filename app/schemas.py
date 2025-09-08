"""
Схемы данных для валидации и сериализации.

Этот модуль содержит Pydantic модели для валидации входных данных
и сериализации выходных данных API.
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

__all__ = [
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductResponse"
]


class ProductBase(BaseModel):
    """
    Базовая схема продукта.

    Используется как основа для других схем продукта.
    """

    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Название продукта",
        examples=["Ноутбук MacBook Pro"]
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Описание продукта",
        examples=["Мощный ноутбук для профессиональной работы"]
    )

    price: float = Field(
        ...,
        gt=0.0,
        description="Цена продукта",
        examples=[999.99]
    )


class ProductCreate(ProductBase):
    """
    Схема для создания нового продукта.

    Наследует все поля от ProductBase.
    """


class ProductUpdate(BaseModel):
    """
    Схема для обновления существующего продукта.

    Все поля опциональны для частичного обновления.
    """

    name: Optional[str] = Field(
        None,
        min_length=1,
        max_length=255,
        description="Название продукта"
    )

    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Описание продукта"
    )

    price: Optional[float] = Field(
        None,
        gt=0.0,
        description="Цена продукта"
    )


class ProductResponse(ProductBase):
    """
    Схема для ответа API с данными продукта.

    Включает все поля из ProductBase плюс идентификатор и временные метки.
    """

    id: int = Field(
        ...,
        description="Уникальный идентификатор продукта"
    )

    created_at: datetime = Field(
        ...,
        description="Дата и время создания продукта"
    )

    updated_at: Optional[datetime] = Field(
        None,
        description="Дата и время последнего обновления продукта"
    )

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "name": "Ноутбук MacBook Pro",
                    "description": "Мощный ноутбук для профессиональной работы",
                    "price": 999.99,
                    "created_at": "2023-01-01T12:00:00",
                    "updated_at": "2023-01-02T14:30:00"
                }
            ]
        }
    }