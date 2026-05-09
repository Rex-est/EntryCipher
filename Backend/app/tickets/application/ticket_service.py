import secrets
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.tickets.domain.entities import Ticket
from app.events.domain.entities import Event
from datetime import datetime
import pyotp

def buy_ticket(db: Session, event_id: int, user_id: int):
    # 1. Verificar si el evento existe
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="El evento solicitado no existe.")

    # 2. Verificar disponibilidad (Seguridad de aforo)
    tickets_sold = db.query(Ticket).filter(Ticket.event_id == event_id).count()
    if tickets_sold >= event.capacity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="¡Sold Out! Ya no quedan entradas disponibles."
        )

    # 3. Generar semilla aleatoria para el QR (16 bytes hexadecimales)
    seed = secrets.token_hex(16)

    new_ticket = Ticket(
        event_id=event_id,
        user_id=user_id,
        qr_seed=seed
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def get_my_tickets(db: Session, user_id: int):
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def get_dynamic_qr_token(db: Session, ticket_code: str, user_id: int):
    # Buscar el ticket para obtener su semilla secreta
    ticket = db.query(Ticket).filter(
        Ticket.ticket_code == ticket_code, 
        Ticket.user_id == user_id
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    # Crear un generador TOTP usando la semilla única del ticket
    # Nota: La semilla debe estar en formato base32 para pyotp
    import base64
    b32_seed = base64.b32encode(ticket.qr_seed.encode()).decode()
    totp = pyotp.TOTP(b32_seed, interval=60) # El código cambia cada 60 segundos
    
    return {
        "dynamic_token": totp.now(),
        "expires_in": totp.interval - (datetime.now().timestamp() % totp.interval)
    }
    
def validate_ticket(db: Session, ticket_code: str):
    # 1. Buscar el ticket por su código único (UUID)
    ticket = db.query(Ticket).filter(Ticket.ticket_code == ticket_code).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="¡ALERTA! Ticket no encontrado en el sistema.")

    # 2. Verificar si ya fue usado (Control de duplicados)
    if ticket.is_used:
        raise HTTPException(
            status_code=400, 
            detail=f"¡ACCESO DENEGADO! Este ticket ya fue validado anteriormente."
        )

    # 3. "Quemar" el ticket (Cambiar estado a usado)
    ticket.is_used = True
    db.commit()
    db.refresh(ticket)
    
    return {
        "status": "SUCCESS",
        "message": "ACCESO AUTORIZADO",
        "ticket_id": ticket.id,
        "validation_time": datetime.utcnow()
    }