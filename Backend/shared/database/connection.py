from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# Forzar codificación UTF-8 para evitar errores de decodificación en Windows
os.environ["PGCLIENTENCODING"] = "utf-8"

# Se lee de la variable de entorno DATABASE_URL (provista por Render), con fallback a la local
SQLALCHEMY_DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://db_entrycipher_i0fm_user:VMaPBkJmTnBfOS7QmLhTF4d1Fc3d2hrD@dpg-d8kvol6rnols73c6qam0-a/db_entrycipher_i0fm"
)

# Render provee la URL de Postgres iniciando con 'postgres://', pero SQLAlchemy >= 1.4 requiere 'postgresql://'
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

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
