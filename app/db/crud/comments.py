import logging

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.consts import LOGGER_ENV_NAME
from app.db import crud, models, schemas
from app.utils import get_env_var

logger = logging.getLogger(get_env_var(LOGGER_ENV_NAME))


async def get_one(session: AsyncSession, comment_id: int) -> models.Comment:
    query = select(models.Comment).where(models.Comment.id == comment_id)
    result = await session.execute(query)
    return result.scalar()


async def get_all(session: AsyncSession, article_id: int) -> list[models.Comment]:
    if not article_id:
        query = select(models.Comment)
        result = await session.execute(query)
        return result.scalars()
    else:
        article = await crud.articles.get_one(session=session, article_id=article_id, fetch_comments=True)
        if not article:
            logger.error(f"tried to get all comments of a non existing article {article_id}")
            raise HTTPException(status_code=404, detail="Article not found")
        else:
            return article.comments


async def create(session: AsyncSession, comment_create: schemas.CommentCreate) -> models.Comment:
    comment = models.Comment(**comment_create.model_dump())
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    return comment
