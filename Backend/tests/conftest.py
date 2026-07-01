import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault(
    "JWT_SECRET_KEY",
    "test-secret-key-only-for-automated-tests-1234567890"
)
os.environ.setdefault("JWT_ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "15")

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from shared.database.connection import Base, get_db
from main import app


# Base de datos SQLite para pruebas
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    from fastapi.testclient import TestClient

    def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()