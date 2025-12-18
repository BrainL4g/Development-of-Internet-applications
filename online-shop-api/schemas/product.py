from pydantic import BaseModel, Field
from typing import Optional

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    stock: int = Field(default=0, ge=0)

class ProductCreateForm(ProductBase):
    """Для POST — принимаем как FormData"""
    pass

class ProductCreate(ProductBase):
    """Для внутренних операций сервиса"""
    pass

class ProductUpdate(ProductBase):
    """Для PUT — частичное обновление"""
    pass

class ProductResponse(ProductBase):
    id: int

    model_config = {
        "from_attributes": True
    }