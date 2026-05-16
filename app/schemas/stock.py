from pydantic import BaseModel
from typing import Optional

class StockCreate(BaseModel):
    name: str
    category: str
    quantity: float
    unit: str
    cost_price: float
    sell_price: float
    reorder_level: float = 5

class StockOut(BaseModel):
    id: int
    name: str
    category: str
    quantity: float
    unit: str
    sell_price: float
    reorder_level: float
    status: str

    model_config = {"from_attributes": True}