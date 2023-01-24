from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # set default to True
    # rating: Optional[int] = None  # set default to none


class PostCreate(PostBase):
    pass
