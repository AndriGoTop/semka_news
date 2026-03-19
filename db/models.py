from datetime import datetime

from sqlmodel import Field, SQLModel


class PostCreate(SQLModel):
    name: str = Field(index=True)
    article: str | None = Field(default=None, index=True)
    image: str | None = Field(default=None)


class Post(PostCreate, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())

class PostPublic(PostCreate):
    id: int


class PostUpdate(PostCreate):
    name: str | None = None
    article: str | None = None
    image: str | None = None
