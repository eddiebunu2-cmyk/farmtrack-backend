from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    note: Optional[str] = None

class ExpenseOut(BaseModel):
    id: int
    category: str
    amount: float
    note: Optional[str]

    model_config = {"from_attributes": True}