from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.core.roles import require_role, OWNER, SUPERADMIN
from app.models.expense import Expense
from app.schemas.expense import ExpenseCreate, ExpenseOut

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/", response_model=ExpenseOut)
def log_expense(data: ExpenseCreate, db: Session = Depends(get_db),
                user = Depends(require_role([OWNER, SUPERADMIN]))):
    expense = Expense(**data.model_dump(), logged_by=user.id)
    db.add(expense)
    db.commit()
    db.refresh(expense)
    return expense

@router.get("/")
def get_expenses(db: Session = Depends(get_db),
                 user = Depends(require_role([OWNER, SUPERADMIN]))):
    return db.query(Expense).order_by(Expense.created_at.desc()).limit(100).all()

@router.get("/month")
def monthly_expenses(db: Session = Depends(get_db),
                     user = Depends(require_role([OWNER, SUPERADMIN]))):
    today = date.today()
    total = db.query(func.sum(Expense.amount)).filter(
        func.extract("month", Expense.created_at) == today.month,
        func.extract("year", Expense.created_at) == today.year
    ).scalar() or 0
    return {"month": today.strftime("%B %Y"), "total_expenses": round(total, 2)}