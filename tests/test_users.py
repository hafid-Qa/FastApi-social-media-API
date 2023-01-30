from app import schemas
from .database import client, session

def test_root(client):
    print("Testing Root")
    res = client.get("/")
    assert res.json() == "to see documentation open: http://localhost:8000/docs or /redoc"


def test_create_user(client):
    res = client.post("/users/", json={"email": "test@example.com", "password": "testpassword", "phone_number": "01"})

    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@example.com"
