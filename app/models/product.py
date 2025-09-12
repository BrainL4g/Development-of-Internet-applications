from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Mapped
from typing import Optional
from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    title: Mapped[str] = Column(String, nullable=False)
    description: Mapped[Optional[str]] = Column(String, nullable=True)
    price: Mapped[float] = Column(Float, nullable=False)
    sku: Mapped[str] = Column(String, unique=True, nullable=False)
