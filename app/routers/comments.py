from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from app.db import schemas
from app.db import crud
from app.db.database import get_db

router = APIRouter(prefix="/comments")


@router.post("/", tags=["comments"], response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    article = crud.articles.get_one(db=db, article_id=comment.article_id)
    if not article:
        raise HTTPException(status_code=400, detail="Comment is related to an unknown article")
    return crud.comments.create(db=db, comment=comment)


@router.get("/", tags=["comments"], response_model=list[schemas.Comment])
def get_comments(article_id: int = None, db: Session = Depends(get_db)):
    comments = crud.comments.get_all(db=db, article_id=article_id)
    return comments


@router.get("/{comment_id}", tags=["comments"], response_model=schemas.Comment)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.comments.get_one(db=db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="comment not found")
    return comment
