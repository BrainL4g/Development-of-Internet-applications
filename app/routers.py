from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import Account, AccountCreate, AccountUpdate
from app.crud import get_accounts, get_account, create_account, update_account, delete_account
from app.database import get_db

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[Account])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_accounts(db, skip=skip, limit=limit)

@router.get("/{account_id}", response_model=Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.post("/", response_model=Account)
def create_account_endpoint(account: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, account)

@router.put("/{account_id}", response_model=Account)
def update_account_endpoint(account_id: int, account: AccountUpdate, db: Session = Depends(get_db)):
    db_account = update_account(db, account_id, account)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@router.delete("/{account_id}", response_model=Account)
def delete_account_endpoint(account_id: int, db: Session = Depends(get_db)):
    db_account = delete_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account