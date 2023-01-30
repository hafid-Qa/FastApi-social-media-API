from app import schemas
from jose import jwt
from .database import client, session
import pytest
from app.config import settings


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "testpassword", "phone_number": "01"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_root(client):
    print("Testing Root")
    res = client.get("/")
    assert res.json() == "to see documentation open: http://localhost:8000/docs or /redoc"


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "testpassword", "phone_number": "01"})

    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@example.com"


def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password": test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
