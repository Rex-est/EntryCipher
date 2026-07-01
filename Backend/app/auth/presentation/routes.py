from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from shared.database.connection import get_db
from shared.security.rate_limit import limiter
from app.auth.application import auth_service
from app.auth.schemas.request import UserCreate, UserLogin, TokenResponse


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
def register(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    auth_service.register_user(db, user)

    return {"message": "Usuario creado exitosamente"}


@router.post("/login", response_model=TokenResponse)
@limiter.limit("10/minute")
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_credentials = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    return auth_service.authenticate_user(db, user_credentials)