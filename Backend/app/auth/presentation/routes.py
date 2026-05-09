from fastapi import APIRouter, Depends
# 👇 Esta es la clave: el formulario estándar de OAuth2
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from shared.database.connection import get_db
from app.auth.schemas.request import UserCreate, UserLogin, TokenResponse
from app.auth.application import auth_service

router = APIRouter()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    auth_service.register_user(db, user)
    return {"message": "Usuario creado exitosamente"}

@router.post("/login", response_model=TokenResponse)
# 👇 Cambiamos 'user: UserLogin' por 'form_data: OAuth2PasswordRequestForm'
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Swagger guarda el correo en un campo llamado 'username'
    # Lo convertimos a tu esquema para que tu lógica no cambie
    user_credentials = UserLogin(email=form_data.username, password=form_data.password)
    return auth_service.authenticate_user(db, user_credentials)