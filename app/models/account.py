from sqlalchemy import Column, Integer, String, Float, CheckConstraint
from app.database import Base


class Account(Base):
  __tablename__ = "accounts"
  __table_args__ = (CheckConstraint("balance >= 0", name="balance_non_negative"),)

  id = Column(Integer, primary_key=True, index=True)
  number = Column(String, unique=True, index=True, nullable=False)
  balance = Column(Float, index=True, nullable=False)
  owner = Column(String, index=True)
