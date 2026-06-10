from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from shared.database.connection import get_db
from app.auth.domain.entities import User
from app.auth.infrastructure.security import SECRET_KEY, ALGORITHM

# Esto le dice a Swagger UI dónde debe ir a buscar el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Desencriptamos el token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        jti: str = payload.get("jti") # Nueva: ID de sesión
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Buscamos al usuario en la base de datos
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    # --- ANTI-MULTISESIÓN ---
    # Si el JTI del token no coincide con el último guardado, la sesión expiró por otro inicio
    if user.last_jti and jti != user.last_jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tu sesión ha sido cerrada porque se inició sesión en otro dispositivo."
        )

    return user

# El guardián estricto: Solo deja pasar si eres ADMIN
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación denegada. Se requieren privilegios de Administrador."
        )
    return current_user

def require_operator(current_user: User = Depends(get_current_user)):
    # Verificamos que el rol sea OPERATOR o ADMIN
    if current_user.role.value not in ["OPERATOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de Operador o Administrador."
        )
    return current_user