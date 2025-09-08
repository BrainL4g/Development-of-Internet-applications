"""
Модели данных для приложения интернет-магазина.

Этот модуль содержит определения таблиц базы данных с использованием SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from .database import Base

__all__ = ["Product"]


class Product(Base):
    """
    Модель продукта в интернет-магазине.

    Представляет таблицу 'products' в базе данных, содержащую информацию о товарах.
    """

    __tablename__ = "products"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор продукта"
    )

    name = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Название продукта"
    )

    description = Column(
        String,
        nullable=True,
        comment="Описание продукта"
    )

    # Цена продукта
    price = Column(
        Float(precision=2),
        nullable=False,
        comment="Цена продукта"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Дата и время создания продукта"
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        comment="Дата и время последнего обновления продукта"
    )

    def __repr__(self) -> str:
        """
        Строковое представление объекта Product.

        Возвращает:
            str: Строковое представление объекта с основной информацией
        """
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
