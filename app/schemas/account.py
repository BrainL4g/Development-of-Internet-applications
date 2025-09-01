from typing import Optional
from pydantic import BaseModel, field_validator


class AccountBase(BaseModel):
  number: Optional[str] = None
  balance: Optional[float] = None
  owner: Optional[str] = None

  @field_validator("balance")
  @classmethod
  def non_negative(cls, v: Optional[float]) -> Optional[float]:
    if v is not None and v < 0: raise ValueError("Balance must be non-negative")
    return v


class AccountCreate(AccountBase):
  number: str
  balance: float


class AccountUpdate(AccountBase): ...


class Account(AccountBase):
  id: int
  model_config = {"from_attributes": True}
