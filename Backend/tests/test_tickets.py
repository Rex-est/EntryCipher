import pytest
from app.auth.application import auth_service
from app.auth.schemas.request import UserCreate
from app.events.infrastructure import repository as event_repo
from app.events.schemas.request import EventCreate, EventZoneCreate, PricingTierCreate
from app.tickets.application import ticket_service
from fastapi import HTTPException
from datetime import datetime

def test_intelligent_purchase_logic(db):
    # 1. Crear Usuario
    user = auth_service.register_user(db, UserCreate(email="buyer@test.com", password="pwd", dni="111222"))

    # 2. Crear Evento Complejo con Tiers
    event_data = EventCreate(
        name="Test Fest", location="Local", date=datetime.utcnow(),
        max_tickets_per_user=2,
        zones=[
            EventZoneCreate(
                name="VIP", total_capacity=10, is_numbered=False,
                tiers=[
                    PricingTierCreate(name="Early", price=50.0, stock_limit=1),
                    PricingTierCreate(name="General", price=100.0, stock_limit=5)
                ]
            )
        ]
    )
    db_event = event_repo.create_event(db, event_data)
    zone_id = db_event.zones[0].id

    # 3. COMPRA 1: Debería asignar precio Early Bird (50.0)
    ticket1 = ticket_service.buy_ticket(db, db_event.id, user.id, zone_id)
    assert ticket1.price_paid == 50.0

    # 4. COMPRA 2: El Early Bird tiene stock 1, así que ahora debería saltar a General (100.0)
    ticket2 = ticket_service.buy_ticket(db, db_event.id, user.id, zone_id)
    assert ticket2.price_paid == 100.0

    # 5. COMPRA 3: Límite por usuario es 2. Debería lanzar error.
    with pytest.raises(HTTPException) as exc:
        ticket_service.buy_ticket(db, db_event.id, user.id, zone_id)
    assert "límite máximo" in exc.value.detail

def test_sold_out_zone(db):
    user = auth_service.register_user(db, UserCreate(email="soldout@test.com", password="pwd", dni="333"))
    
    # Evento con una sola entrada en stock total
    event_data = EventCreate(
        name="SoldOut Show", location="Local", date=datetime.utcnow(),
        zones=[
            EventZoneCreate(
                name="General", total_capacity=1, is_numbered=False,
                tiers=[PricingTierCreate(name="Fase 1", price=10, stock_limit=1)]
            )
        ]
    )
    db_event = event_repo.create_event(db, event_data)
    zone_id = db_event.zones[0].id

    # Agotar stock
    ticket_service.buy_ticket(db, db_event.id, user.id, zone_id)

    # Intentar comprar sin stock
    user2 = auth_service.register_user(db, UserCreate(email="user2@test.com", password="pwd", dni="444"))
    with pytest.raises(HTTPException) as exc:
        ticket_service.buy_ticket(db, db_event.id, user2.id, zone_id)
    assert "Sold Out" in exc.value.detail
