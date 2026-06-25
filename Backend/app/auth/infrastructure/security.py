from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

import secrets

# NOTA DE CIBERSEGURIDAD: En producción, esto debe venir de un archivo .env
SECRET_KEY = "Firma_Super_Secreta_SafeTicket_2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120 # El token expira en 2 horas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Agregamos JTI para identificar esta sesión única
    to_encode.update({"exp": expire, "jti": secrets.token_hex(8)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt