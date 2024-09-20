from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import crud, schemas
from app.db.database import get_session

router = APIRouter(prefix="/users")


@router.post("/", tags=["users"], response_model=schemas.User)
async def create_user(user_create: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await crud.users.get_by_name(session=session, name=user_create.name)
    if existing_user:
        raise HTTPException(status_code=400, detail="User already registered")
    existing_email = await crud.users.get_by_email(session=session, email=user_create.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.users.create(session=session, user_create=user_create)


@router.get("/", tags=["users"], response_model=list[schemas.User])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await crud.users.get_all(session=session)
    return users


@router.get("/{user_id}", tags=["users"], response_model=schemas.User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await crud.users.get_one(session=session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
