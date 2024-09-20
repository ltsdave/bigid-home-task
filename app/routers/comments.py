from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud, schemas
from app.db.database import get_session

router = APIRouter(prefix="/comments")


@router.post("/", tags=["comments"], response_model=schemas.Comment)
async def create_comment(comment_create: schemas.CommentCreate, session: AsyncSession = Depends(get_session)):
    article = await crud.articles.get_one(session=session, article_id=comment_create.article_id)
    if not article:
        raise HTTPException(status_code=400, detail="Comment is related to a non existing article")
    return await crud.comments.create(session=session, comment_create=comment_create)


@router.get("/", tags=["comments"], response_model=list[schemas.Comment])
async def get_comments(article_id: int = None, session: AsyncSession = Depends(get_session)):
    comments = await crud.comments.get_all(session=session, article_id=article_id)
    return comments


@router.get("/{comment_id}", tags=["comments"], response_model=schemas.Comment)
async def get_comment(comment_id: int, session: AsyncSession = Depends(get_session)):
    comment = await crud.comments.get_one(session=session, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
