from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from shared.database.connection import get_db
from app.auth.domain.entities import User
from app.auth.infrastructure.security import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")
        jti: str = payload.get("jti")

        if not email or not jti:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()

    # Bloquea cuentas inexistentes o suspendidas.
    if user is None or not user.is_active:
        raise credentials_exception

    # Solo permite la última sesión activa del usuario.
    if not user.last_jti or jti != user.last_jti:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La sesión no es válida o fue reemplazada por un nuevo inicio de sesión."
        )

    return user


def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.value != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación denegada. Se requieren privilegios de Administrador."
        )

    return current_user


def require_operator(current_user: User = Depends(get_current_user)):
    if current_user.role.value not in ["OPERATOR", "ADMIN"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado. Se requieren permisos de Operador o Administrador."
        )

    return current_user