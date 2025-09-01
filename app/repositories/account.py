from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate
from app.core.exceptions import AccountNotFound, AccountExists


class AccountRepository:
  def __init__(self, db: Session):
    self.db = db

  def all(self, skip=0, limit=100):
    return self.db.query(Account).offset(skip).limit(limit).all()

  def get(self, account_id: int) -> Account:
    if account := self.db.get(Account, account_id): return account
    raise AccountNotFound

  def create(self, data: AccountCreate) -> Account:
    account = Account(**data.model_dump())
    self.db.add(account)
    try:
      self.db.commit()
      self.db.refresh(account)
      return account
    except IntegrityError:
      self.db.rollback()
      raise AccountExists

  def update(self, account_id: int, data: AccountUpdate) -> Account:
    acc = self.get(account_id)
    for k, v in data.model_dump(exclude_unset=True).items(): setattr(acc, k, v)
    self.db.commit();
    self.db.refresh(acc);
    return acc

  def delete(self, account_id: int) -> None:
    acc = self.get(account_id)
    self.db.delete(acc);
    self.db.commit()
