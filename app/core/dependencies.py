from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.account import AccountRepository

DbSession = Annotated[Session, Depends(get_db)]
AccountRepo = Annotated[AccountRepository, Depends(lambda db: AccountRepository(db))]
