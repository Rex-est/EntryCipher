import pytest
import time
from app.auth.application import auth_service
from app.auth.schemas.request import UserCreate, UserLogin
from app.auth.domain.entities import User
from app.auth.infrastructure import security
from fastapi import HTTPException
from jose import jwt

def test_anti_multisession_logic(db):
    # 1. Registrar un usuario
    user_data = UserCreate(email="test@example.com", password="password123", dni="12345678X")
    auth_service.register_user(db, user_data)

    # 2. Primer login (Sesión 1)
    login_data = UserLogin(email="test@example.com", password="password123")
    res1 = auth_service.authenticate_user(db, login_data)
    token1 = res1["access_token"]
    
    # Obtener el JTI de la sesión 1
    decoded1 = jwt.decode(token1, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    jti1 = decoded1.get("jti")
    
    # Verificar que el JTI se guardó en la DB
    user = db.query(User).filter(User.email == "test@example.com").first()
    assert user.last_jti == jti1

    # 3. Segundo login (Sesión 2 - Invalida la anterior)
    res2 = auth_service.authenticate_user(db, login_data)
    token2 = res2["access_token"]
    
    # Obtener el JTI de la sesión 2
    decoded2 = jwt.decode(token2, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    jti2 = decoded2.get("jti")
    
    assert jti1 != jti2 # Deben ser diferentes
    
    # Verificar que el JTI en DB ahora es el de la sesión 2
    db.refresh(user)
    assert user.last_jti == jti2
    assert user.last_jti != jti1

def test_invalid_credentials(db):
    # Intentar loguear usuario inexistente
    login_data = UserLogin(email="no@existe.com", password="password")
    with pytest.raises(HTTPException) as exc:
        auth_service.authenticate_user(db, login_data)
    assert exc.value.status_code == 401
def test_access_token_uses_fifteen_minute_expiration():
    token = security.create_access_token({"sub": "expiration-test"})

    decoded = jwt.decode(
        token,
        security.SECRET_KEY,
        algorithms=[security.ALGORITHM]
    )

    remaining_seconds = decoded["exp"] - time.time()

    assert security.ACCESS_TOKEN_EXPIRE_MINUTES == 15
    assert remaining_seconds <= 15 * 60
    assert remaining_seconds > 14 * 60