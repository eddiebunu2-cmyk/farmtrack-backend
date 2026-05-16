from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.roles import require_role, OWNER, SUPERADMIN, EMPLOYEE
from app.models.stock import StockItem
from app.schemas.stock import StockCreate, StockOut

router = APIRouter(prefix="/stock", tags=["Stock"])

def compute_status(item: StockItem) -> str:
    if item.quantity <= 0:
        return "out"
    if item.quantity <= item.reorder_level:
        return "low"
    return "ok"

@router.get("/", response_model=list[StockOut])
def get_stock(db: Session = Depends(get_db),
              user = Depends(require_role([SUPERADMIN, OWNER, EMPLOYEE]))):
    items = db.query(StockItem).all()
    result = []
    for item in items:
        out = StockOut(
            id=item.id, name=item.name, category=item.category,
            quantity=item.quantity, unit=item.unit,
            sell_price=item.sell_price, reorder_level=item.reorder_level,
            status=compute_status(item)
        )
        result.append(out)
    return result

@router.post("/")
def add_stock(data: StockCreate, db: Session = Depends(get_db),
              user = Depends(require_role([OWNER, SUPERADMIN]))):
    item = StockItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"message": f"{item.name} added to stock", "id": item.id}

@router.patch("/{item_id}")
def update_stock(item_id: int, data: StockCreate, db: Session = Depends(get_db),
                 user = Depends(require_role([OWNER, SUPERADMIN]))):
    item = db.query(StockItem).filter(StockItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Stock item not found")
    for field, value in data.model_dump().items():
        setattr(item, field, value)
    db.commit()
    return {"message": f"{item.name} updated"}