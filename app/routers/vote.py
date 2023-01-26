from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter

router = APIRouter(prefix="/vote", tags=["Vote"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote():
    print("Vote")
