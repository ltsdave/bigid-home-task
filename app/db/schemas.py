from datetime import datetime

from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str
    article_id: int


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class ArticleBase(BaseModel):
    title: str
    content: str
    author_id: int


class ArticleCreate(ArticleBase):
    pass


class Article(ArticleBase):
    id: int
    publish_date: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
