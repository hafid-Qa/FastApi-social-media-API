from fastapi.testclient import TestClient
from app.main import app
import pytest
from app import models
from app.oauth2 import create_access_token
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db


SQLALCHEMY_DATABASE_URL = (
    f"postgresql://@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@example.com", "password": "correctpassword", "phone_number": "01"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user_non_main(client):
    user_data = {"email": "testother@example.com", "password": "correctpassword", "phone_number": "01"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@pytest.fixture
def test_posts(test_user, session, test_user_non_main):
    posts_data = [
        {
            "title": "title 1",
            "content": "content 1",
            "user_id": test_user["id"],
        },
        {
            "title": "title 1",
            "content": "content 2",
            "user_id": test_user["id"],
        },
        {
            "title": "title 1",
            "content": "content 2",
            "user_id": test_user_non_main["id"],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    posts_map = map(create_post_model, posts_data)
    posts = list(posts_map)
    session.add_all(posts)
    session.commit()
    db_posts = session.query(models.Post).all()
    return db_posts
