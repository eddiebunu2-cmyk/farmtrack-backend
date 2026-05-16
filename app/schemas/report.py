from pydantic import BaseModel

class DailySummary(BaseModel):
    date: str
    total_sales: float
    total_expenses: float
    profit: float

class MonthlySummary(BaseModel):
    month: str
    total_sales: float
    total_expenses: float
    profit: float
    top_selling_item: str