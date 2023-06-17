from calendar import c
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr
from typing_extensions import Literal


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    phone_number: Optional["str"]


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # set default to True
    # rating: Optional[int] = None  # set default to none

    class Config:
        orm_mode = False


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    user_id: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class PostWithVoteResponse(BaseModel):
    Post: PostResponse
    votes: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    id: Optional[int] = None

    class Config:
        orm_mode = True


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]

    class Config:
        orm_mode = False
