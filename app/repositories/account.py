from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.account import Account
from app.schemas.account import AccountCreate, AccountUpdate
from app.core.exceptions import AccountExistsException, AccountNotFoundException

class AccountRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_accounts(self, skip: int = 0, limit: int = 100) -> List[Account]:
        return self.db.query(Account).offset(skip).limit(limit).all()

    def get_account(self, account_id: int) -> Account:
        account: Account | None = self.db.query(Account).filter(Account.id == account_id).first()
        if not account:
            raise AccountNotFoundException()
        return account

    def create_account(self, account: AccountCreate) -> Account:
        if self.db.query(Account).filter(Account.number == account.number).first():
            raise AccountExistsException()
        db_account: Account = Account(**account.model_dump())
        self.db.add(db_account)
        try:
            self.db.commit()
            self.db.refresh(db_account)
        except IntegrityError:
            self.db.rollback()
            raise AccountExistsException()
        return db_account

    def update_account(self, account_id: int, account: AccountUpdate) -> Account:
        db_account: Account = self.get_account(account_id)
        for key, value in account.model_dump(exclude_unset=True).items():
            setattr(db_account, key, value)
        self.db.commit()
        self.db.refresh(db_account)
        return db_account

    def delete_account(self, account_id: int) -> Account:
        db_account: Account = self.get_account(account_id)
        self.db.delete(db_account)
        self.db.commit()
        return db_account