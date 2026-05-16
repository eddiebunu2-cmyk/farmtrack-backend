from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import date
from app.core.database import get_db
from app.core.roles import require_role, OWNER, SUPERADMIN
from app.models.sale import Sale
from app.models.expense import Expense
from app.schemas.report import DailySummary, MonthlySummary

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/today", response_model=DailySummary)
def daily_summary(db: Session = Depends(get_db),
                  user = Depends(require_role([OWNER, SUPERADMIN]))):
    today = date.today()
    sales = db.query(func.sum(Sale.total_price)).filter(
        func.date(Sale.sold_at) == today).scalar() or 0
    expenses = db.query(func.sum(Expense.amount)).filter(
        func.date(Expense.created_at) == today).scalar() or 0
    return DailySummary(
        date=str(today),
        total_sales=round(sales, 2),
        total_expenses=round(expenses, 2),
        profit=round(sales - expenses, 2)
    )

@router.get("/month", response_model=MonthlySummary)
def monthly_summary(db: Session = Depends(get_db),
                    user = Depends(require_role([OWNER, SUPERADMIN]))):
    today = date.today()
    sales = db.query(func.sum(Sale.total_price)).filter(
        func.extract("month", Sale.sold_at) == today.month,
        func.extract("year", Sale.sold_at) == today.year
    ).scalar() or 0
    expenses = db.query(func.sum(Expense.amount)).filter(
        func.extract("month", Expense.created_at) == today.month,
        func.extract("year", Expense.created_at) == today.year
    ).scalar() or 0
    return MonthlySummary(
        month=today.strftime("%B %Y"),
        total_sales=round(sales, 2),
        total_expenses=round(expenses, 2),
        profit=round(sales - expenses, 2),
        top_selling_item="Eggs"
    )