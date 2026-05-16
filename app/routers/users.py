from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.roles import require_role, OWNER, SUPERADMIN
from app.core.auth import hash_password
from app.models.user import User
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["Users"])

class UserCreate(BaseModel):
    name: str
    phone: str
    pin: str
    role: str = "employee"

@router.get("/")
def list_users(db: Session = Depends(get_db),
               user = Depends(require_role([OWNER, SUPERADMIN]))):
    return db.query(User).filter(User.is_active == True).all()

@router.post("/")
def create_user(data: UserCreate, db: Session = Depends(get_db),
                user = Depends(require_role([OWNER, SUPERADMIN]))):
    if data.role == SUPERADMIN and user.role != SUPERADMIN:
        raise HTTPException(status_code=403, detail="Only superadmin can create another superadmin")
    existing = db.query(User).filter(User.phone == data.phone).first()
    if existing:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    new_user = User(
        name=data.name,
        phone=data.phone,
        pin_hash=hash_password(data.pin),
        role=data.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": f"User {new_user.name} created", "id": new_user.id}

@router.delete("/{user_id}")
def deactivate_user(user_id: int, db: Session = Depends(get_db),
                    user = Depends(require_role([OWNER, SUPERADMIN]))):
    target = db.query(User).filter(User.id == user_id).first()
    if not target:
        raise HTTPException(status_code=404, detail="User not found")
    target.is_active = False
    db.commit()
    return {"message": f"{target.name} has been deactivated"}