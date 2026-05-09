from sqlalchemy.orm import Session
from app.auth.domain.entities import User
from app.auth.schemas.request import UserCreate
from app.auth.infrastructure.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    # Por defecto creamos a todos como USER. El admin se asigna por base de datos.
    db_user = User(email=user.email, hashed_password=hashed_password, dni=user.dni)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user