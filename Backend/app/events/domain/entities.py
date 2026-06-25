from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from shared.database.connection import Base
from datetime import datetime

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    location = Column(String, nullable=False)
    date = Column(DateTime, nullable=False) # Fecha del evento
    
    # Metadatos de publicación
    banner_url = Column(String, nullable=True)
    max_tickets_per_user = Column(Integer, default=4) # Límite de compra por usuario
    start_presale_date = Column(DateTime, nullable=True)
    start_sale_date = Column(DateTime, nullable=True)
    end_publish_date = Column(DateTime, nullable=True) # Fecha de cierre de ventas
    
    terms_and_conditions = Column(String, nullable=True)
    
    # Redes sociales (JSON string o campos simples por ahora)
    social_links = Column(String, nullable=True) 

    # Compatibilidad con el modelo anterior (Legacy)
    capacity = Column(Integer, nullable=True) 
    price = Column(Float, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relaciones
    zones = relationship("EventZone", back_populates="event", cascade="all, delete-orphan")

class EventZone(Base):
    __tablename__ = "event_zones"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    name = Column(String, nullable=False) # Platinum, VIP, General
    total_capacity = Column(Integer, nullable=False)
    is_numbered = Column(Boolean, default=False)

    # Relaciones
    event = relationship("Event", back_populates="zones")
    tiers = relationship("PricingTier", back_populates="zone", cascade="all, delete-orphan")

class PricingTier(Base):
    __tablename__ = "pricing_tiers"

    id = Column(Integer, primary_key=True, index=True)
    zone_id = Column(Integer, ForeignKey("event_zones.id"))
    name = Column(String, nullable=False) # Early Bird, Fase 1
    price = Column(Float, nullable=False)
    stock_limit = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)

    # Relaciones
    zone = relationship("EventZone", back_populates="tiers")
