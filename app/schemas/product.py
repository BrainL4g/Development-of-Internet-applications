from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    title: str
    description: str | None = None
    price: float
    sku: str

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    sku: str | None = None

    model_config = ConfigDict(from_attributes=True)


class ProductRead(ProductBase):
    id: int
