from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from app.schemas.account import Account, AccountCreate, AccountUpdate
from app.repositories.account import AccountRepository
from app.core.exceptions import AccountNotFoundException, AccountExistsException
from app.core.dependencies import get_account_repo

AccountRepo = Annotated[AccountRepository, Depends(get_account_repo)]

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[Account])
def read_accounts(repo: AccountRepo, skip: int = 0, limit: int = 100) -> List[Account]:
    return repo.get_accounts(skip=skip, limit=limit)

@router.get("/{account_id}", response_model=Account)
def read_account(account_id: int, repo: AccountRepo) -> Account:
    try:
        return repo.get_account(account_id)
    except AccountNotFoundException:
        raise HTTPException(status_code=404, detail="Account not found")

@router.post("/", response_model=Account)
def create_account(account: AccountCreate, repo: AccountRepo) -> Account:
    try:
        return repo.create_account(account)
    except AccountExistsException:
        raise HTTPException(status_code=400, detail="Account number already exists")

@router.put("/{account_id}", response_model=Account)
def update_account(account_id: int, account: AccountUpdate, repo: AccountRepo) -> Account:
    try:
        return repo.update_account(account_id, account)
    except AccountNotFoundException:
        raise HTTPException(status_code=404, detail="Account not found")

@router.delete("/{account_id}", response_model=Account)
def delete_account(account_id: int, repo: AccountRepo) -> Account:
    try:
        return repo.delete_account(account_id)
    except AccountNotFoundException:
        raise HTTPException(status_code=404, detail="Account not found")