import typer
import asyncio
from db.database import engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from repositories.product_repository import ProductRepository
from models.product import Product

app = typer.Typer(help="Консольные команды для управления товарами в магазине техники")

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Вывод всех товаров
@app.command()
def list_products():
    """Выводит список всех товаров в базе"""
    async def run():
        async with AsyncSessionLocal() as db:
            repo = ProductRepository(db)
            products = await repo.get_all()
            if not products:
                typer.echo("Нет товаров в базе.")
                return
            typer.echo("Список товаров:")
            for p in products:
                desc = f" ({p.description})" if p.description else ""
                typer.echo(f"  ID: {p.id} | {p.name}{desc} | Цена: {p.price} ₽ | На складе: {p.stock} шт.")

    asyncio.run(run())

# Создание нового товара
@app.command()
def create_product(
    name: str = typer.Option(..., "--name", "-n", prompt="Название товара"),
    description: str = typer.Option(None, "--description", "-d", prompt="Описание (опционально)"),
    price: float = typer.Option(..., "--price", "-p", prompt="Цена (руб.)"),
    stock: int = typer.Option(0, "--stock", "-s", prompt="Количество на складе")
):
    """Создаёт новый товар"""
    async def run():
        async with AsyncSessionLocal() as db:
            repo = ProductRepository(db)
            new_product = Product(name=name, description=description or None, price=price, stock=stock)
            created = await repo.create(new_product)
            typer.echo(f"Товар успешно создан! ID: {created.id}")

    asyncio.run(run())

# Просмотр одного товара
@app.command()
def show_product(product_id: int = typer.Argument(..., help="ID товара")):
    """Показывает информацию о товаре по ID"""
    async def run():
        async with AsyncSessionLocal() as db:
            repo = ProductRepository(db)
            product = await repo.get_by_id(product_id)
            if not product:
                typer.echo(f"Товар с ID {product_id} не найден.", err=True)
                raise typer.Exit(code=1)
            desc = f" ({product.description})" if product.description else ""
            typer.echo(f"Товар ID: {product.id}")
            typer.echo(f"  Название: {product.name}{desc}")
            typer.echo(f"  Цена: {product.price} ₽")
            typer.echo(f"  На складе: {product.stock} шт.")

    asyncio.run(run())

# Обновление товара
@app.command()
def update_product(
    product_id: int = typer.Argument(..., help="ID товара для обновления"),
    name: str = typer.Option(None, "--name", "-n"),
    description: str = typer.Option(None, "--description", "-d"),
    price: float = typer.Option(None, "--price", "-p"),
    stock: int = typer.Option(None, "--stock", "-s")
):
    """Обновляет данные товара по ID"""
    async def run():
        async with AsyncSessionLocal() as db:
            repo = ProductRepository(db)
            product = await repo.get_by_id(product_id)
            if not product:
                typer.echo(f"Товар с ID {product_id} не найден.", err=True)
                raise typer.Exit(code=1)

            if name is not None:
                product.name = name
            if description is not None:
                product.description = description
            if price is not None:
                product.price = price
            if stock is not None:
                product.stock = stock

            updated = await repo.update(product)
            typer.echo(f"Товар ID {updated.id} успешно обновлён!")

    asyncio.run(run())

# Удаление товара
@app.command()
def delete_product(product_id: int = typer.Argument(..., help="ID товара для удаления")):
    """Удаляет товар по ID"""
    async def run():
        async with AsyncSessionLocal() as db:
            repo = ProductRepository(db)
            product = await repo.get_by_id(product_id)
            if not product:
                typer.echo(f"Товар с ID {product_id} не найден.", err=True)
                raise typer.Exit(code=1)

            if typer.confirm(f"Вы уверены, что хотите удалить товар '{product.name}' (ID: {product_id})?"):
                await repo.delete(product)
                typer.echo(f"Товар ID {product_id} успешно удалён.")
            else:
                typer.echo("Удаление отменено.")

    asyncio.run(run())

if __name__ == "__main__":
    app()