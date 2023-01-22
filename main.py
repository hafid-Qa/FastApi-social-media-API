from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str


@app.get("/")
async def root():
    return {"message": "Hello Wor"}


@app.get("/posts")
def get_posts():
    return {"data": "bunch of posts"}


# title str, content str
@app.post("/posts/new")
def create_post(new_post: Post):
    print(new_post)
    return  f'title: {new_post.title} content: {new_post.content}'
   
