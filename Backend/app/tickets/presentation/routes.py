from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from shared.database.connection import get_db
from shared.security.dependencies import get_current_user
from app.auth.domain.entities import User
from app.tickets.schemas.request import TicketPurchase, TicketResponse
from app.tickets.application import ticket_service
from shared.security.dependencies import require_operator

router = APIRouter()

@router.post("/buy", response_model=TicketResponse, summary="Comprar una entrada")
def purchase_ticket(data: TicketPurchase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Pasamos el event_id, user_id y zone_id a la lógica de negocio
    return ticket_service.buy_ticket(db, data.event_id, current_user.id, data.zone_id)

@router.get("/my-tickets", response_model=List[TicketResponse], summary="Ver mis entradas compradas")
def list_my_tickets(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ticket_service.get_my_tickets(db, current_user.id)

@router.post("/validate/{ticket_code}", summary="Validar y quemar un ticket")
def validate_qr(
    ticket_code: str, 
    db: Session = Depends(get_db), 
    staff_user: User = Depends(require_operator) # <--- Ahora usa require_operator
):
    # staff_user ahora representa al Operador que está escaneando
    print(f"Ticket validado por el operador: {staff_user.email}")
    return ticket_service.validate_ticket(db, ticket_code)

@router.get("/generate-qr/{ticket_code}", summary="Obtener código dinámico para el QR")
def get_qr_code(ticket_code: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return ticket_service.get_dynamic_qr_token(db, ticket_code, current_user.id)