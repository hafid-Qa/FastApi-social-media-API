from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Wor"}


@app.get("/posts")
def get_posts():
    return {"data": "bunch of posts"}
