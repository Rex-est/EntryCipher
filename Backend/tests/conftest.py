import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from shared.database.connection import Base
from main import app
from shared.database.connection import get_db

# Base de datos de prueba (In-Memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Crear tablas antes de cada test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Limpiar tablas después de cada test
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    from fastapi.testclient import TestClient
    
    # Sobrescribir la dependencia get_db
    def override_get_db():
        try:
            yield db
        finally:
            pass
            
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield client
    app.dependency_overrides.clear()
