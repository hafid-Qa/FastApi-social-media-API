from typing import List, Optional
from app import schemas


def test_gel_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert len(res.json()) == len(test_posts)
    posts = res.json()
    for post in posts:
        schemas.PostWithVoteResponse(**post)
    assert res.status_code == 200
