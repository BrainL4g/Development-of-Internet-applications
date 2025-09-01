from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.account import Account, AccountCreate, AccountUpdate
from app.core.dependencies import AccountRepo
from app.core.exceptions import AccountNotFound, AccountExists

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/", response_model=List[Account])
def list_accounts(repo: AccountRepo, skip: int = 0, limit: int = 100): return repo.all(skip, limit)


@router.get("/{account_id}", response_model=Account)
def get_account(account_id: int, repo: AccountRepo):
  try:
    return repo.get(account_id)
  except AccountNotFound:
    raise HTTPException(404, "Account not found")


@router.post("/", response_model=Account, status_code=201)
def create_account(account: AccountCreate, repo: AccountRepo):
  try:
    return repo.create(account)
  except AccountExists:
    raise HTTPException(400, "Account already exists")


@router.put("/{account_id}", response_model=Account)
def update_account(account_id: int, account: AccountUpdate, repo: AccountRepo):
  try:
    return repo.update(account_id, account)
  except AccountNotFound:
    raise HTTPException(404, "Account not found")


@router.delete("/{account_id}", status_code=204)
def delete_account(account_id: int, repo: AccountRepo):
  try:
    repo.delete(account_id)
  except AccountNotFound:
    raise HTTPException(404, "Account not found")
