from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


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


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
