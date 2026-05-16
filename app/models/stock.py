from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class StockItem(Base):
    __tablename__ = "stock_items"

    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    category      = Column(String, nullable=False)
    quantity      = Column(Float, default=0)
    unit          = Column(String, default="units")
    cost_price    = Column(Float, default=0)
    sell_price    = Column(Float, default=0)
    reorder_level = Column(Float, default=5)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())