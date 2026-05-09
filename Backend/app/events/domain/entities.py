from sqlalchemy import Column, Integer, String, DateTime, Float
from shared.database.connection import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)