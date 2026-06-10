from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- Tiers ---
class PricingTierBase(BaseModel):
    name: str
    price: float
    stock_limit: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_active: bool = True

class PricingTierCreate(PricingTierBase):
    pass

class PricingTierResponse(PricingTierBase):
    id: int
    class Config:
        from_attributes = True

# --- Zonas ---
class EventZoneBase(BaseModel):
    name: str
    total_capacity: int
    is_numbered: bool = False

class EventZoneCreate(EventZoneBase):
    tiers: List[PricingTierCreate]

class EventZoneResponse(EventZoneBase):
    id: int
    tiers: List[PricingTierResponse]
    class Config:
        from_attributes = True

# --- Evento ---
class EventBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    date: Optional[datetime] = None
    banner_url: Optional[str] = None
    max_tickets_per_user: Optional[int] = 4
    start_presale_date: Optional[datetime] = None
    start_sale_date: Optional[datetime] = None
    end_publish_date: Optional[datetime] = None
    terms_and_conditions: Optional[str] = None
    social_links: Optional[str] = None

class EventCreate(EventBase):
    name: str # Nombre sigue siendo obligatorio al crear
    location: str # Ubicación sigue siendo obligatoria al crear
    date: datetime # Fecha sigue siendo obligatoria al crear
    
    # Soporte para creación simple (Legacy)
    capacity: Optional[int] = None
    price: Optional[float] = None
    
    # Soporte para creación avanzada
    zones: Optional[List[EventZoneCreate]] = None

class EventResponse(EventBase):
    id: int
    capacity: Optional[int] = None
    price: Optional[float] = None
    zones: List[EventZoneResponse] = []
    
    class Config:
        from_attributes = True 
