from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from shared.database.connection import get_db
from shared.security.dependencies import require_admin
from app.auth.domain.entities import User
from app.events.domain.entities import Event
from app.tickets.domain.entities import Ticket


router = APIRouter()


@router.get("/analytics", summary="Obtener analíticas en tiempo real para el Dashboard")
def get_dashboard_analytics(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    total_sales = db.query(Ticket).count()

    revenue = db.query(
        func.sum(Event.price)
    ).join(
        Ticket,
        Event.id == Ticket.event_id
    ).scalar() or 0

    active_events = db.query(Event).count()

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
def list_buyers(
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    buyers = db.query(User).filter(User.role == "USER").all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "dni": user.dni,
            "is_active": user.is_active
        }
        for user in buyers
    ]


@router.post("/users/{user_id}/toggle-status", summary="Activar o suspender un comprador")
def toggle_user_status(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(require_admin)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )

    user.is_active = not user.is_active

    # Al suspender una cuenta, invalida su sesión activa.
    if not user.is_active:
        user.last_jti = None

    db.commit()
    db.refresh(user)

    return {
        "message": "Estado actualizado",
        "is_active": user.is_active
    }