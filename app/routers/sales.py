from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.core.roles import require_role, OWNER, SUPERADMIN, EMPLOYEE
from app.models.sale import Sale
from app.models.stock import StockItem
from app.schemas.sale import SaleCreate, SaleOut

router = APIRouter(prefix="/sales", tags=["Sales"])

@router.post("/", response_model=SaleOut)
def record_sale(data: SaleCreate, db: Session = Depends(get_db),
                user = Depends(require_role([SUPERADMIN, OWNER, EMPLOYEE]))):
    item = db.query(StockItem).filter(StockItem.id == data.item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Stock item not found")
    if item.quantity < data.quantity:
        raise HTTPException(status_code=400,
                            detail=f"Not enough stock. Only {item.quantity} {item.unit} left")
    total = round(item.sell_price * data.quantity, 2)
    sale = Sale(
        item_id=data.item_id,
        quantity=data.quantity,
        total_price=total,
        payment_type=data.payment_type,
        customer_id=data.customer_id,
        sold_by=user.id
    )
    item.quantity -= data.quantity
    db.add(sale)
    db.commit()
    db.refresh(sale)
    return sale

@router.get("/")
def get_sales(db: Session = Depends(get_db),
              user = Depends(require_role([OWNER, SUPERADMIN]))):
    return db.query(Sale).order_by(Sale.sold_at.desc()).limit(100).all()

@router.get("/today")
def todays_total(db: Session = Depends(get_db),
                 user = Depends(require_role([OWNER, SUPERADMIN]))):
    today = date.today()
    total = db.query(func.sum(Sale.total_price)).filter(
        func.date(Sale.sold_at) == today).scalar() or 0
    count = db.query(Sale).filter(func.date(Sale.sold_at) == today).count()
    return {"date": str(today), "total_sales": round(total, 2), "transactions": count}