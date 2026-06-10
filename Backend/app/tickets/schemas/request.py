from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketPurchase(BaseModel):
    event_id: int
    zone_id: int

class TicketResponse(BaseModel):
    id: int
    ticket_code: str
    event_id: int
    zone_id: Optional[int] = None
    price_paid: Optional[float] = None
    purchased_at: datetime
    is_used: bool

    class Config:
        from_attributes = True
        
