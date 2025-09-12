from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.product_crud import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead


class ProductService:
    def __init__(self, db: AsyncSession):
        self.repo = ProductRepository(db)

    async def list_products(self) -> list[ProductRead]:
        return await self.repo.get_all()

    async def get_product(self, product_id: int) -> ProductRead:
        if product := await self.repo.get_by_id(product_id):
            return product
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Product not found")

    async def create_product(self, payload: ProductCreate) -> ProductRead:
        if await self.repo.get_by_sku(payload.sku):
            raise HTTPException(status.HTTP_409_CONFLICT, "SKU already exists")
        return await self.repo.create(payload)

    async def update_product(self, product_id: int, payload: ProductUpdate) -> ProductRead:
        product = await self.get_product(product_id)
        if payload.sku and payload.sku != product.sku and await self.repo.get_by_sku(payload.sku):
            raise HTTPException(status.HTTP_409_CONFLICT, "SKU already exists")
        return await self.repo.update(product, payload)

    async def delete_product(self, product_id: int) -> None:
        await self.repo.delete(await self.get_product(product_id))
