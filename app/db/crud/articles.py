from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db import crud, models, schemas


def get_one(db: Session, article_id: int, show_relation: bool = False) -> models.Article:
    if show_relation:
        return (
            db.query(models.Article)
            .filter(models.Article.id == article_id)
            .options(joinedload(models.Article.comments))
            .first()
        )
    else:
        return db.query(models.Article).filter(models.Article.id == article_id).first()


def get_by_title(db: Session, title: str) -> models.Article:
    return db.query(models.Article).filter(models.Article.title == title).first()


def get_all(db: Session, author_id: int) -> list[models.Article]:
    if not author_id:
        return db.query(models.Article).all()
    else:
        user = crud.users.get_one(db=db, user_id=author_id, show_relation=True)
        if not user:
            raise HTTPException(status_code=404, detail="author not found")
        else:
            return user.articles


def create(db: Session, article: schemas.ArticleCreate) -> models.Article:
    db_article = models.Article(**article.model_dump(), publish_date=datetime.now())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
