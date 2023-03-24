from pydantic import BaseModel


class PostIn(BaseModel):
    title: str
    text: str
    is_published: bool


class Post(BaseModel):
    id: int
    title: str
    text: str
    is_published: bool
