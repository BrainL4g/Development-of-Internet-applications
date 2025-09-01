from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, index=True, unique=True)
    balance = Column(Float, index=True)
    owner = Column(String, index=True)