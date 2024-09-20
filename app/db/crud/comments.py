from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db import crud, models, schemas


def get_one(db: Session, comment_id: int) -> models.Comment:
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_all(db: Session, article_id: int) -> list[models.Comment]:
    if not article_id:
        return db.query(models.Comment).all()
    else:
        article = crud.articles.get_one(db=db, article_id=article_id, show_relation=True)
        if not article:
            raise HTTPException(status_code=404, detail="article not found")
        else:
            return article.comments


def create(db: Session, comment: schemas.CommentCreate) -> models.Comment:
    db_article = models.Comment(**comment.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article
