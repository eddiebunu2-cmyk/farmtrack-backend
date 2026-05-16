from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SaleCreate(BaseModel):
    item_id: int
    quantity: float
    payment_type: str = "cash"
    customer_id: Optional[int] = None

class SaleOut(BaseModel):
    id: int
    item_id: int
    quantity: float
    total_price: float
    payment_type: str
    sold_at: datetime

    model_config = {"from_attributes": True}