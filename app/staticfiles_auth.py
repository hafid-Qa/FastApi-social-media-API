from contextlib import contextmanager

from fastapi import HTTPException, Request, status
from fastapi.staticfiles import StaticFiles

from .config import settings
from .database import get_db
from .oauth2 import get_current_user


@contextmanager
def db_scope():
    """Provide a transactional scope around a series of operations."""
    db = next(get_db())
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


async def verify_user(request: Request):
    try:
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = token.split("Bearer ")[1]
        with db_scope() as db:
            get_current_user(token=str(token), db=db, token_helper=TokenHelper(settings))
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error")


class AuthStaticFiles(StaticFiles):
    """Static files with authentication using JWT"""

    def __init__(self, *args, **kwargs) -> None:

        super().__init__(*args, **kwargs)

    async def __call__(self, scope, receive, send) -> None:

        assert scope["type"] == "http"

        request = Request(scope, receive)
        await verify_user(request)
        await super().__call__(scope, receive, send)
