from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from typing import List, Optional


class ProductRepository:
    def __init__(self, db: AsyncSession):
        self.db: AsyncSession = db

    async def get_all(self) -> List[Product]:
        result = await self.db.execute(select(Product))
        return result.scalars().all()

    async def get_by_id(self, product_id: int) -> Optional[Product]:
        return await self.db.get(Product, product_id)

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        result = await self.db.execute(select(Product).where(Product.sku == sku))
        return result.scalars().first()

    async def create(self, obj_in: ProductCreate) -> Product:
        db_obj = Product(**obj_in.model_dump())
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: Product, obj_in: ProductUpdate) -> Product:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete(self, db_obj: Product) -> None:
        await self.db.delete(db_obj)
        await self.db.commit()
