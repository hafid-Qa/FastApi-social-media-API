from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
from app.database import Base


# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

SQLALCHEMY_DATABASE_URL = f"postgresql://@{settings.database_hostname}/{settings.database_name}_test"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)
# Base = declarative_base()

# Dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_root():
    print("Testing Root")
    res = client.get("/")
    assert res.json() == "to see documentation open: http://localhost:8000/docs or /redoc"


def test_create_user():
    res = client.post("/users/", json={"email": "test@example.com", "password": "testpassword", "phone_number": "01"})

    new_user = schemas.UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == "test@example.com"
