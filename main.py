from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # set default to True
    rating: Optional[int] = None  # set default to none


my_posts = [{"id": 1, "title": "post 1", "content": "content 1"}, {"id": 2, "title": "post 2", "content": "content 2"}]


@app.get("/")
async def root():
    return {"message": "Hello Wor"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# title str, content str
@app.post("/posts")
def create_post(post: Post):
    my_posts.append(post.dict())  # covert pydantic model to dict

    return {"msg": "post created successfully"}
