from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # set default to True
    # rating: Optional[int] = None  # set default to none


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fast_api_dev", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established...")
        break
    except Exception as error:
        print({"error": error})
        time.sleep(2)

my_posts = [{"id": 1, "title": "post 1", "content": "content 1"}, {"id": 2, "title": "post 2", "content": "content 2"}]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# title str, content str
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):  # perform validation and convert id to int at the same time
    cursor.execute("""SELECT * FROM posts WHERE id= %s""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")
        # one way to handling errors
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"msg": f"post with id:{id} Not Found"}
        # second way to handle errors
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""", (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(
        """UPDATE posts SET title=%s , content= %s, published= %s WHERE id=%s RETURNING *""",
        (
            post.title,
            post.content,
            post.published,
            str(id),
        ),
    )
    updated_post = cursor.fetchone()
    conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} Not Found")
    return {"data": updated_post}
