from pydantic import BaseModel, Field, PositiveInt
from enum import Enum



class OperationType(str, Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAW = "WITHDRAW"



class WalletIn(BaseModel):
    operation_type: OperationType
    amount: PositiveInt


class WalletOut(BaseModel):
    wallet_uuid: str
    balance: int

