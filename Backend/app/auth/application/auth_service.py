from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.auth.infrastructure import repository, security
from app.auth.schemas.request import UserCreate, UserLogin


def register_user(db: Session, user: UserCreate):
    # Regla 1: No correos duplicados
    db_user = repository.get_user_by_email(db, email=user.email)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    return repository.create_user(db, user)


def authenticate_user(db: Session, user: UserLogin):
    db_user = repository.get_user_by_email(db, email=user.email)

    # Valida existencia, estado de cuenta y contraseña
    if (
        not db_user
        or not db_user.is_active
        or not security.verify_password(
            user.password,
            db_user.hashed_password
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    # Generar token con identidad y rol
    access_token = security.create_access_token(
        data={
            "sub": db_user.email,
            "role": db_user.role.value
        }
    )

    # Guardar el JTI de la sesión activa
    from jose import jwt

    decoded = jwt.decode(
        access_token,
        security.SECRET_KEY,
        algorithms=[security.ALGORITHM]
    )

    db_user.last_jti = decoded.get("jti")
    db.add(db_user)

    db.commit()
    db.refresh(db_user)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role.value
    }