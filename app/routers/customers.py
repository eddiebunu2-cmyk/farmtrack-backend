from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.roles import require_role, OWNER, SUPERADMIN
from app.models.customer import Customer
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/customers", tags=["Customers"])

class CustomerCreate(BaseModel):
    name: str
    phone: Optional[str] = None

@router.get("/")
def get_customers(db: Session = Depends(get_db),
                  user = Depends(require_role([OWNER, SUPERADMIN]))):
    return db.query(Customer).filter(
        Customer.balance_owed > 0).order_by(Customer.balance_owed.desc()).all()

@router.post("/")
def add_customer(data: CustomerCreate, db: Session = Depends(get_db),
                 user = Depends(require_role([OWNER, SUPERADMIN]))):
    customer = Customer(**data.model_dump())
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return {"message": f"Customer {customer.name} added", "id": customer.id}

@router.patch("/{customer_id}/paid")
def mark_paid(customer_id: int, db: Session = Depends(get_db),
              user = Depends(require_role([OWNER, SUPERADMIN]))):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.balance_owed = 0
    db.commit()
    return {"message": f"{customer.name} marked as fully paid"}