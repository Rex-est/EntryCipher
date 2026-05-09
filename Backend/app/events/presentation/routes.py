from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from shared.database.connection import get_db
from app.events.schemas.request import EventCreate, EventResponse
from app.events.infrastructure import repository
from shared.security.dependencies import get_current_user, require_admin
from app.auth.domain.entities import User

router = APIRouter()

# CUALQUIER USUARIO LOGUEADO PUEDE VER LOS EVENTOS
@router.get("/", response_model=List[EventResponse], summary="Ver todos los eventos")
def list_events(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return repository.get_all_events(db)

# SOLO EL ADMIN PUEDE CREAR EVENTOS
@router.post("/", response_model=EventResponse, summary="Crear un evento (Solo Admin)")
def create_new_event(event: EventCreate, db: Session = Depends(get_db), admin_user: User = Depends(require_admin)):
    return repository.create_event(db, event)