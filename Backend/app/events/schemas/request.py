from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
    name: str
    date: datetime
    location: str
    capacity: int
    price: float

class EventResponse(EventCreate):
    id: int
    
    class Config:
        from_attributes = True 