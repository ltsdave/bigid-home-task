from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from app.db import schemas
from app.db import crud
from app.db.database import get_db

router = APIRouter(prefix="/articles")


@router.post("/", tags=["articles"], response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    article = crud.articles.get_by_title(db=db, title=article.title)
    if article:
        raise HTTPException(status_code=400, detail="Article already published")
    user = crud.users.get_one(db=db, user_id=article.author_id)
    if not user:
        raise HTTPException(status_code=400, detail="Article is written by an unknown user")
    return crud.articles.create(db=db, article=article)


@router.get("/", tags=["articles"], response_model=list[schemas.Article])
def get_articles(author_id: int = None, db: Session = Depends(get_db)):
    articles = crud.articles.get_all(db=db, author_id=author_id)
    return articles


@router.get("/{article_id}", tags=["articles"], response_model=schemas.Article)
def get_article(article_id: int, db: Session = Depends(get_db)):
    article = crud.articles.get_one(db=db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
