from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # set default to True
    rating: Optional[int] = None  # set default to none


my_posts = [{"id": 1, "title": "post 1", "content": "content 1"}, {"id": 2, "title": "post 2", "content": "content 2"}]


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post


def find_index_post(id):
    for i, post in enumerate(my_posts):
        if post["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello Wor"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# title str, content str
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()  # covert pydantic model to dict
    post_dict["id"] = randrange(0, 100000)
    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):  # perform validation and convert id to int at the same time
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")
        # one way to handling errors
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg": f"post with id:{id} Not Found"}
        # second way to handle errors
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # find index of the id
    index = find_index_post(id)
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
