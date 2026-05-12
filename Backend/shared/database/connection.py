from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# NOTA: En producción esto debe ir en variables de entorno (.env)
# Por ahora usaremos una cadena de conexión local genérica
SQLALCHEMY_DATABASE_URL = "postgresql://db_entrycipher_user:h5ttJsfns5GS5QmZFHPka2ERf6adBSyX@dpg-d818si37uimc73852du0-a.oregon-postgres.render.com/db_entrycipher"

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
