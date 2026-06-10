from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Forzar codificación UTF-8 para evitar errores de decodificación en Windows
os.environ["PGCLIENTENCODING"] = "utf-8"

# NOTA: En producción esto debe ir en variables de entorno (.env)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./prod.db")

# Si es SQLite, necesitamos argumentos especiales
if SQLALCHEMY_DATABASE_URL.startswith("sqlite"):
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependencia para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
