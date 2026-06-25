import secrets
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.tickets.domain.entities import Ticket
from app.events.domain.entities import Event, EventZone, PricingTier
from datetime import datetime
import pyotp

def buy_ticket(db: Session, event_id: int, user_id: int, zone_id: int):
    # 1. Verificar si el evento existe
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="El evento solicitado no existe.")

    # 2. Verificar si la zona existe y pertenece al evento
    zone = db.query(EventZone).filter(EventZone.id == zone_id, EventZone.event_id == event_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="La zona seleccionada no existe para este evento.")

    # 2.5 Verificar límite de compra por usuario
    user_tickets_count = db.query(Ticket).filter(
        Ticket.event_id == event_id, 
        Ticket.user_id == user_id
    ).count()
    
    if user_tickets_count >= (event.max_tickets_per_user or 4):
        raise HTTPException(
            status_code=400, 
            detail=f"Has alcanzado el límite máximo de {event.max_tickets_per_user} entradas para este evento."
        )

    # 3. Verificar fechas de venta
    now = datetime.utcnow()
    if event.start_presale_date and now < event.start_presale_date:
        raise HTTPException(status_code=400, detail="La venta aún no ha comenzado.")
    if event.end_publish_date and now > event.end_publish_date:
        raise HTTPException(status_code=400, detail="La venta para este evento ha finalizado.")

    # 4. Encontrar el Tier (Fase de precio) activo
    # Criterio: El primer tier activo que tenga stock
    active_tier = None
    tiers = db.query(PricingTier).filter(
        PricingTier.zone_id == zone_id,
        PricingTier.is_active == True
    ).order_by(PricingTier.price.asc()).all()

    for tier in tiers:
        # Contar cuántos tickets se han vendido en este tier
        # (Para una implementación más robusta, el Ticket debería tener un tier_id)
        # Por ahora, comparamos contra el stock_limit de la zona o del tier
        sold_in_tier = db.query(Ticket).filter(
            Ticket.zone_id == zone_id,
            Ticket.price_paid == tier.price # Un proxy para el tier
        ).count()
        
        if sold_in_tier < tier.stock_limit:
            active_tier = tier
            break
    
    if not active_tier:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="¡Sold Out! No hay fases de precio disponibles con stock para esta zona."
        )

    # 5. Generar semilla aleatoria para el QR
    seed = secrets.token_hex(16)

    new_ticket = Ticket(
        event_id=event_id,
        user_id=user_id,
        zone_id=zone_id,
        price_paid=active_tier.price,
        qr_seed=seed
    )
    
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket

def get_my_tickets(db: Session, user_id: int):
    return db.query(Ticket).filter(Ticket.user_id == user_id).all()

def get_dynamic_qr_token(db: Session, ticket_code: str, user_id: int):
    ticket = db.query(Ticket).filter(
        Ticket.ticket_code == ticket_code, 
        Ticket.user_id == user_id
    ).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket no encontrado")

    import base64
    b32_seed = base64.b32encode(ticket.qr_seed.encode()).decode()
    totp = pyotp.TOTP(b32_seed, interval=60)
    
    return {
        "dynamic_token": totp.now(),
        "expires_in": totp.interval - (datetime.now().timestamp() % totp.interval)
    }
    
def validate_ticket(db: Session, ticket_code: str):
    ticket = db.query(Ticket).filter(Ticket.ticket_code == ticket_code).first()
    
    if not ticket:
        raise HTTPException(status_code=404, detail="¡ALERTA! Ticket no encontrado.")

    if ticket.is_used:
        raise HTTPException(status_code=400, detail="¡ACCESO DENEGADO! Ya usado.")

    ticket.is_used = True
    db.commit()
    db.refresh(ticket)
    
    return {
        "status": "SUCCESS",
        "message": "ACCESO AUTORIZADO",
        "ticket_id": ticket.id,
        "validation_time": datetime.utcnow()
    }
