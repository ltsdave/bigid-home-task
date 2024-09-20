from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.db import crud, models, schemas


async def get_one(session: AsyncSession, article_id: int, fetch_comments: bool = False) -> models.Article:
    if fetch_comments:
        query = (
            select(models.Article)
            .where(models.Article.id == article_id)
            .options(joinedload(models.Article.comments))
        )
    else:
        query = select(models.Article).where(models.Article.id == article_id)
    result = await session.execute(query)
    return result.scalar()


async def get_by_title(session: AsyncSession, title: str) -> models.Article:
    query = select(models.Article).where(models.Article.title == title)
    result = await session.execute(query)
    return result.scalar()


async def get_all(session: AsyncSession, author_id: int) -> list[models.Article]:
    if not author_id:
        query = select(models.Article)
        result = await session.execute(query)
        return result.scalars()
    else:
        user = await crud.users.get_one(session=session, user_id=author_id, fetch_articles=True)
        if not user:
            raise HTTPException(status_code=404, detail="author not found")
        else:
            return user.articles


async def create(session: AsyncSession, article_create: schemas.ArticleCreate) -> models.Article:
    article = models.Article(**article_create.model_dump(), publish_date=datetime.now())
    session.add(article)
    await session.commit()
    await session.refresh(article)
    return article
