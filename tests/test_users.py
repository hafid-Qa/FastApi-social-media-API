from app import schemas
from jose import jwt
from app.config import settings
import pytest


def test_root(client):
    print("Testing Root")
    res = client.get("/")
    assert res.json() == "to see documentation open: http://localhost:8000/docs or /redoc"


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test@example.com", "password": "correctpassword", "phone_number": "01"}
    )

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


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@example.com", "wrongpassword", 403),
        ("wrongemail@example.com", "correctpassword", 403),
        ("wrongemail@example.com", "wrongpassword", 403),
        (None, "correctpassword", 422),
        ("test@example.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    if res.status_code == 403:
        assert res.json().get("detail") == "Invalid Credentials"
