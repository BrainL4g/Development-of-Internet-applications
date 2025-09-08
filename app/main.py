# app/main.py
"""
Shop API entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .database import engine
from . import models
from .routers import products

# Ensure database tables are created
models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Online Shop API", version="1.0.0")

# CORS middleware for client integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router, prefix="/api/v1", tags=["products"])

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "Online Shop API is running"}