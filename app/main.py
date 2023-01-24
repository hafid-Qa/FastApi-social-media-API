from fastapi import FastAPI, Response, status, HTTPException, Depends
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
import time
from .database import engine
from .routers import post, user


models.Base.metadata.create_all(bind=engine)
app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host="localhost", database="fast_api_dev", cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection established...")
        break
    except Exception as error:
        print({"error": error})
        time.sleep(2)


@app.get("/")
async def root():
    return "to see documentation open: http://localhost:8000/docs "


app.include_router(post.router)
app.include_router(user.router)
