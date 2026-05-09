from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from shared.database.connection import Base
from datetime import datetime
import uuid

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    # Generamos un código único para el ticket (ej: '550e8400-e29b-41d4...')
    ticket_code = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    purchased_at = Column(DateTime, default=datetime.utcnow)
    is_used = Column(Boolean, default=False)
    # Semilla aleatoria que usaremos para el QR dinámico después
    qr_seed = Column(String, nullable=False)