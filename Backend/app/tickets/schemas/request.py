from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TicketPurchase(BaseModel):
    event_id: int

class TicketResponse(BaseModel):
    id: int
    ticket_code: str
    event_id: int
    purchased_at: datetime
    qr_seed: str
    is_used: bool

    class Config:
        from_attributes = True
        
