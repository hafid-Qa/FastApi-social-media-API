from app import schemas
import pytest


def test_gel_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    posts = res.json()
    for post in posts:
        schemas.PostWithVoteResponse(**post)
    assert res.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"


def test_unauthorized_user_get_one_posts(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"


def test_get_one_posts_not_exit(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/100")
    assert res.status_code == 404
    assert res.json().get("detail") == "Post with id:100 Not Found"


def test_get_one(authorized_client, test_posts, test_user):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostWithVoteResponse(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.user_id == test_user["id"]


@pytest.mark.parametrize(
    "title ,content,published",
    [
        ("title 1", "content 1", True),
        ("title 2", "content 2", True),
        ("title 3", "content 3", False),
    ],
)
def test_create_post(authorized_client, test_user, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "test title", "content": "test content"})

    created_post = schemas.PostResponse(**res.json())
    assert res.status_code == 201
    assert created_post.title == "test title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.user_id == test_user["id"]


def test_unauthorized_user_get_create_posts(client, test_posts):
    res = client.post("/posts/", json={"title": "test title", "content": "test content"})
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"


def test_unauthorized_user_delete_posts(client, test_posts):
    res = client.delete("/posts/{test_posts[0].id}")
    assert res.status_code == 401
    assert res.json().get("detail") == "Not authenticated"
