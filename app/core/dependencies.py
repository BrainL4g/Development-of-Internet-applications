from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.account import AccountRepository

DbSession = Annotated[Session, Depends(get_db)]

def get_account_repo(db: DbSession) -> AccountRepository:
    return AccountRepository(db)