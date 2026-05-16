from app.core.database import SessionLocal, Base, engine
from app.core.auth import hash_password
from app.models.user import User
import app.models.stock
import app.models.sale
import app.models.expense
import app.models.chicken
import app.models.customer

# Create all tables first
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Check if superadmin already exists
existing = db.query(User).filter(User.phone == "+263771234567").first()

if existing:
    print("Superadmin already exists")
else:
    superadmin = User(
        name="Tapiwa",
        phone="+263771234567",
        pin_hash=hash_password("1234"),
        role="superadmin"
    )
    db.add(superadmin)
    db.commit()
    db.refresh(superadmin)
    print(f"Superadmin created — ID: {superadmin.id}, Name: {superadmin.name}")

db.close()