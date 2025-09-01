from typing import Optional

from pydantic import BaseModel, field_validator

class AccountBase(BaseModel):
    number: str
    balance: float
    owner: Optional[str] = None

    @field_validator('balance')

    @classmethod
    def validate_balance(cls, v: float) -> float:
        if v < 0:
            raise ValueError('Balance must be non-negative')
        return v

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class Account(AccountBase):
    id: int

    model_config = {"from_attributes": True}