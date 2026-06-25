from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Dict
from shared.database.connection import get_db
from shared.security.dependencies import require_admin
from app.auth.domain.entities import User
from app.events.domain.entities import Event, EventZone, PricingTier
from app.tickets.domain.entities import Ticket
from sqlalchemy import func

router = APIRouter()

@router.get("/analytics", summary="Obtener analíticas en tiempo real para el Dashboard")
def get_dashboard_analytics(db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    # 1. Ventas Totales
    total_sales = db.query(Ticket).count()
    
    # 2. Ingresos Brutos (Calculado sobre tickets vendidos y sus precios en ese momento)
    # Por ahora simplificamos: sumamos el precio de los eventos de los tickets
    # En un sistema real, el Ticket debería guardar el precio exacto al que se vendió
    revenue = db.query(func.sum(Event.price)).join(Ticket, Event.id == Ticket.event_id).scalar() or 0
    
    # 3. Eventos Activos
    active_events = db.query(Event).count()
    
    # 4. Datos para el gráfico de velocidad (Simulado: tickets por día los últimos 7 días)
    # En una implementación real usaríamos group_by(func.date(Ticket.purchased_at))
    sales_velocity = [
        {"date": "2024-05-01", "sales": 10},
        {"date": "2024-05-02", "sales": 25},
        {"date": "2024-05-03", "sales": 15},
        {"date": "2024-05-04", "sales": 45},
        {"date": "2024-05-05", "sales": 30},
    ]

    return {
        "total_sales": total_sales,
        "revenue": revenue,
        "active_events": active_events,
        "sales_velocity": sales_velocity
    }

@router.get("/buyers", summary="Listado de todos los compradores")
def list_buyers(db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    buyers = db.query(User).filter(User.role == "USER").all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "dni": u.dni,
            "is_active": u.is_active
        } for u in buyers
    ]

@router.post("/users/{user_id}/toggle-status", summary="Activar/Suspender un comprador")
def toggle_user_status(user_id: int, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "Usuario no encontrado"}
    
    user.is_active = not user.is_active
    db.commit()
    return {"message": "Estado actualizado", "is_active": user.is_active}
