from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id           = Column(Integer, primary_key=True, index=True)
    item_id      = Column(Integer, ForeignKey("stock_items.id"), nullable=False)
    quantity     = Column(Float, nullable=False)
    total_price  = Column(Float, nullable=False)
    payment_type = Column(String, default="cash")
    customer_id  = Column(Integer, ForeignKey("customers.id"), nullable=True)
    sold_by      = Column(Integer, ForeignKey("users.id"), nullable=False)
    sold_at      = Column(DateTime(timezone=True), server_default=func.now())