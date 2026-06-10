from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Forzar codificación UTF-8 para evitar errores de decodificación en Windows
os.environ["PGCLIENTENCODING"] = "utf-8"

# NOTA: En producción esto debe ir en variables de entorno (.env)
# Por ahora usaremos una cadena de conexión local genérica
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Gappi532915@localhost:5432/entrycipher"

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
