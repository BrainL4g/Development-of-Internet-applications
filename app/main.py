"""
Основной файл приложения FastAPI для интернет-магазина.

Этот файл содержит настройку FastAPI приложения, подключение маршрутов,
настройку CORS и управление жизненным циклом приложения.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .database import async_engine
from . import models
from .routers import products

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Контекстный менеджер для управления жизненным циклом приложения.

    Выполняет инициализацию базы данных при запуске приложения.

    Аргументы:
        app (FastAPI): Экземпляр FastAPI приложения
    """
    async with async_engine.begin() as conn:
        # Создаем все таблицы в базе данных
        await conn.run_sync(models.Base.metadata.create_all)
    yield


app = FastAPI(
    title="Online Shop API",
    version="1.0.0",
    lifespan=lifespan,
    description="API для интернет-магазина",
    contact={
        "name": "Разработчик",
        "email": "developer@example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex="https?://(localhost|127.0.0.1)(:[0-9]+)?",
)

# Подключение маршрутов продуктов
app.include_router(products.router, prefix="/products", tags=["products"])


@app.get("/", summary="Корневая конечная точка", tags=["health"])
async def root() -> dict[str, str]:
    """
    Корневая конечная точка API.

    Возвращает приветственное сообщение о состоянии приложения.

    Возвращает:
        dict[str, str]: Словарь с сообщением о состоянии приложения
    """
    return {"message": "Online Shop API is running"}


@app.get("/health", summary="Проверка состояния", tags=["health"])
async def health_check() -> dict[str, str]:
    """
    Конечная точка для проверки состояния приложения.

    Возвращает:
        dict[str, str]: Словарь с информацией о состоянии приложения
    """
    return {"status": "healthy", "message": "Application is running"}
