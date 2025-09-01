from typing import Optional

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import Session

from app.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id: int = Column(Integer, primary_key=True, index=True)
    number: str = Column(String, index=True, unique=True)
    balance: float = Column(Float, index=True)
    owner: Optional[str] = Column(String, index=True)

    def get_balance(self) -> float:
        return self.balance

    def set_balance(self, value: float, db: Session) -> None:
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.balance = value
        db.commit()
        db.refresh(self)

    def get_owner(self) -> Optional[str]:
        return self.owner

    def set_owner(self, value: Optional[str], db: Session) -> None:
        self.owner = value
        db.commit()
        db.refresh(self)