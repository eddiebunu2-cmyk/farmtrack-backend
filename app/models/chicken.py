from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class Flock(Base):
    __tablename__ = "flock"

    id         = Column(Integer, primary_key=True, index=True)
    bird_type  = Column(String, nullable=False)
    count      = Column(Integer, default=0)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class EggLog(Base):
    __tablename__ = "egg_logs"

    id        = Column(Integer, primary_key=True, index=True)
    count     = Column(Integer, nullable=False)
    logged_at = Column(DateTime(timezone=True), server_default=func.now())

class FeedLog(Base):
    __tablename__ = "feed_logs"

    id         = Column(Integer, primary_key=True, index=True)
    amount_kg  = Column(Float, nullable=False)
    feed_type  = Column(String, nullable=True)
    logged_at  = Column(DateTime(timezone=True), server_default=func.now())

class MortalityLog(Base):
    __tablename__ = "mortality_logs"

    id         = Column(Integer, primary_key=True, index=True)
    bird_count = Column(Integer, nullable=False)
    cause      = Column(String, nullable=True)
    logged_at  = Column(DateTime(timezone=True), server_default=func.now())