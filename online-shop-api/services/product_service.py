from fastapi import HTTPException
from models.product import Product
from schemas.product import ProductCreate, ProductUpdate, ProductResponse
from repositories.product_repository import ProductRepository
from typing import List

class ProductService:
    def __init__(self, repo: ProductRepository):
        self.repo = repo

    async def get_all(self) -> List[ProductResponse]:
        products = await self.repo.get_all()
        return [ProductResponse.model_validate(p) for p in products]

    async def get_by_id(self, product_id: int) -> ProductResponse:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return ProductResponse.model_validate(product)

    async def create(self, data: ProductCreate) -> ProductResponse:
        product = Product(**data.model_dump())
        created = await self.repo.create(product)
        return ProductResponse.model_validate(created)

    async def update(self, product_id: int, data: ProductUpdate) -> ProductResponse:
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(product, key, value)

        updated = await self.repo.update(product)
        return ProductResponse.model_validate(updated)

    async def delete(self, product_id: int):
        product = await self.repo.get_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await self.repo.delete(product)
        return {"detail": "Product deleted successfully"}