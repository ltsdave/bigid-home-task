from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud, schemas
from app.db.database import get_session

router = APIRouter(prefix="/articles")


@router.post("/", tags=["articles"], response_model=schemas.Article)
async def create_article(article_create: schemas.ArticleCreate, session: AsyncSession = Depends(get_session)):
    existing_article = await crud.articles.get_by_title(session=session, title=article_create.title)
    if existing_article:
        raise HTTPException(status_code=400, detail="Article already published")
    user = await crud.users.get_one(session=session, user_id=article_create.author_id)
    if not user:
        raise HTTPException(status_code=400, detail="Article is written by a non existing author")
    return await crud.articles.create(session=session, article_create=article_create)


@router.get("/", tags=["articles"], response_model=list[schemas.Article])
async def get_articles(author_id: int = None, session: AsyncSession = Depends(get_session)):
    articles = await crud.articles.get_all(session=session, author_id=author_id)
    return articles


@router.get("/{article_id}", tags=["articles"], response_model=schemas.Article)
async def get_article(article_id: int, session: AsyncSession = Depends(get_session)):
    article = await crud.articles.get_one(session=session, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article
