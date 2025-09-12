from fastapi import APIRouter, status, Form
from typing import Optional
from app.schemas.product import ProductCreateForm, ProductRead, ProductUpdate
from app.deps import ProductServiceDep

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductRead])
async def list_products(service: ProductServiceDep):
    return await service.list_products()


@router.get("/{product_id}", response_model=ProductRead)
async def get_product(product_id: int, service: ProductServiceDep):
    return await service.get_product(product_id)


@router.post(
    "/",
    response_model=ProductRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать продукт (FormData)"
)
async def create_product(
        service: ProductServiceDep,
        title: str = Form(..., description="Название продукта"),
        description: Optional[str] = Form(None, description="Описание продукта"),
        price: float = Form(..., description="Цена продукта"),
        sku: str = Form(..., description="Уникальный SKU продукта")
):
    payload = ProductCreateForm(
        title=title,
        description=description,
        price=price,
        sku=sku
    )
    return await service.create_product(payload)


@router.put("/{product_id}", response_model=ProductRead, summary="Обновить продукт (JSON)")
async def update_product(product_id: int, payload: ProductUpdate, service: ProductServiceDep):
    return await service.update_product(product_id, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить продукт")
async def delete_product(product_id: int, service: ProductServiceDep):
    await service.delete_product(product_id)
