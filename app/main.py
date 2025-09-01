from fastapi import FastAPI
from app.routers.account import router

app = FastAPI(title="Bank API", version="1.1.2")
app.include_router(router)
