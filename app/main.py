from fastapi import FastAPI
from app.database import engine
from app.models.account import Account
from app.routers.account import router

Account.metadata.create_all(bind=engine)

app = FastAPI(title="Bank API", version="1.0.0")

app.include_router(router)