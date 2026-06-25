from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.auth.infrastructure import repository, security
from app.auth.schemas.request import UserCreate, UserLogin

def register_user(db: Session, user: UserCreate):
    # Regla 1: No correos duplicados
    db_user = repository.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    return repository.create_user(db, user)

def authenticate_user(db: Session, user: UserLogin):
    db_user = repository.get_user_by_email(db, email=user.email)
    
    # Regla 2: Validar existencia y contraseña segura
    if not db_user or not security.verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales incorrectas"
        )
    
    # Generar el Token con los claims de seguridad (identidad y rol)
    access_token = security.create_access_token(
        data={"sub": db_user.email, "role": db_user.role.value}
    )

    # --- ANTI-MULTISESIÓN ---
    # Extraemos el JTI generado para guardarlo como la sesión activa
    from jose import jwt
    decoded = jwt.decode(access_token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    db_user.last_jti = decoded.get("jti")
    db.add(db_user) 
    
    db.commit()
    db.refresh(db_user)

    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "role": db_user.role.value
    }
