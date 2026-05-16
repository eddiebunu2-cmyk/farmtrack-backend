from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.routers import auth, users, stock, sales, expenses, customers, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FarmTrack API",
    description="Backend for Mai's Farm and Shop Manager",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(stock.router)
app.include_router(sales.router)
app.include_router(expenses.router)
app.include_router(customers.router)
app.include_router(reports.router)

@app.get("/")
def root():
    return {"message": "FarmTrack API is running"}