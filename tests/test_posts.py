from typing import List, Optional
from app import schemas


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


