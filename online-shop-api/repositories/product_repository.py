from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from models.product import Product
from typing import List, Optional


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[Product]:
        result = await self.db.execute(select(Product).order_by(Product.id))
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def create(self, product: Product) -> Product:
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def update(self, product: Product) -> Product:
        await self.db.commit()
        await self.db.refresh(product)
        return product

    async def delete(self, product: Product):
        await self.db.delete(product)
        await self.db.commit()
