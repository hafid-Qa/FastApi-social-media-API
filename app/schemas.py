from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # set default to True
    # rating: Optional[int] = None  # set default to none
