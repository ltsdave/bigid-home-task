from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from app.db import models, schemas


async def get_one(session: AsyncSession, user_id: int, fetch_articles: bool = False) -> models.User:
    if fetch_articles:
        query = select(models.User).where(models.User.id == user_id).options(joinedload(models.User.articles))
    else:
        query = select(models.User).where(models.User.id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def get_by_name(session: AsyncSession, name: str) -> models.User:
    query = select(models.User).where(models.User.name == name)
    result = await session.execute(query)
    return result.scalar()


async def get_by_email(session: AsyncSession, email: str) -> models.User:
    query = select(models.User).where(models.User.email == email)
    result = await session.execute(query)
    return result.scalar()


async def get_all(session: AsyncSession) -> list[models.User]:
    query = select(models.User)
    result = await session.execute(query)
    return result.scalars().all()


async def create(session: AsyncSession, user_create: schemas.UserCreate) -> models.User:
    user = models.User(**user_create.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
