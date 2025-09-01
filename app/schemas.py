from pydantic import BaseModel

class AccountBase(BaseModel):
    number: str
    balance: float
    owner: str | None = None

class AccountCreate(AccountBase):
    pass

class AccountUpdate(AccountBase):
    pass

class Account(AccountBase):
    id: int

    model_config = {"from_attributes": True}