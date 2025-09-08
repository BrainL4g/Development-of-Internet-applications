# app/schemas.py
"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema shared by create and update."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    price: float = Field(..., gt=0.0)


class ProductCreate(ProductBase):
    """Schema for creating a new product."""


class ProductUpdate(ProductBase):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[Optional[str]] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0.0)


class ProductResponse(ProductBase):
    """Schema for product response."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True