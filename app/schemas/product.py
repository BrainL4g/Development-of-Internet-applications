from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    sku: str

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase): ...


class ProductCreateForm(BaseModel):
    title: str = Field(..., description="Название продукта")
    description: Optional[str] = Field(None, description="Описание продукта")
    price: float = Field(..., gt=0, description="Цена продукта (должна быть положительной)")
    sku: str = Field(..., description="Уникальный SKU продукта")

    model_config = ConfigDict(from_attributes=True)


class ProductUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Новое название")
    description: Optional[str] = Field(None, description="Новое описание")
    price: Optional[float] = Field(None, gt=0, description="Новая цена")
    sku: Optional[str] = Field(None, description="Новый SKU")

    model_config = ConfigDict(from_attributes=True)


class ProductRead(ProductBase):
    id: int
