from sqlalchemy import TEXT, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    articles = relationship("Article", back_populates="author", lazy="noload")


class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True, index=True)
    publish_date = Column(DateTime, index=True)
    content = Column(TEXT)
    author_id = Column(Integer, ForeignKey("users.id"))

    author = relationship("User", back_populates="articles")
    comments = relationship("Comment", back_populates="article", lazy="noload")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)
    content = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))

    article = relationship("Article", back_populates="comments")
