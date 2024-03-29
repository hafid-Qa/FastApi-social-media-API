import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routers import auth, post, user, vote
from .staticfiles_auth import AuthStaticFiles

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
# specify the allowed domain to send requests to api
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount(
    "/files",
    AuthStaticFiles(directory="/files"),
    name="static",
)


@app.get("/")
async def root():
    return "to see documentation open: http://localhost:8000/docs or /redoc"


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


def main():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, access_log=True, reload=True)


if __name__ == "__main__":
    main()
