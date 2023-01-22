from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Wor"}


@app.get("/posts")
def get_posts():
    return {"data": "bunch of posts"}


@app.post("/posts/new")
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"message": "post created successfully"}
