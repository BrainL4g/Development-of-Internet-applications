from contextlib import asynccontextmanager
from fastapi import FastAPI
from routes.product_routes import router as product_router
from models.product import Base
from db.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Online Shop API - Техника",
    lifespan=lifespan
)

app.include_router(product_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Online Shop API (техника)"}