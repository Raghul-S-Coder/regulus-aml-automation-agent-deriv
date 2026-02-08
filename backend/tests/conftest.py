import pytest
from fastapi.testclient import TestClient

from app.config.database import Base, SessionLocal, engine
from app.main import create_app


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client():
    app = create_app()
    return TestClient(app)


@pytest.fixture()
def standard_headers():
    return {
        "X-Request-ID": "test-request-id",
        "X-Forwarded-For": "127.0.0.1",
        "X-Device-Id": "test-device",
    }
