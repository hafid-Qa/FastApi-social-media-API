from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import schemas, models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    yield TestClient(app)


def test_root(client):
    print("Testing Root")
    res = client.get("/")
    assert res.json() == "to see documentation open: http://localhost:8000/docs or /redoc"


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "testpassword", "phone_number": "01"})

    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@example.com"
