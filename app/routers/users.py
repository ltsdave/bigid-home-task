import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.consts import LOGGER_ENV_NAME
from app.db import crud, schemas
from app.db.database import get_session
from app.utils import get_env_var

router = APIRouter(prefix="/users")
logger = logging.getLogger(get_env_var(LOGGER_ENV_NAME))


@router.post("/", tags=["users"], response_model=schemas.User)
async def create_user(user_create: schemas.UserCreate, session: AsyncSession = Depends(get_session)):
    existing_user = await crud.users.get_by_name(session=session, name=user_create.name)
    if existing_user:
        logger.error(f"tried to create an already registered user {user_create.name}")
        raise HTTPException(status_code=400, detail="User already registered")
    existing_email = await crud.users.get_by_email(session=session, email=user_create.email)
    if existing_email:
        logger.error(f"tried to create a user with a taken email {user_create.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.users.create(session=session, user_create=user_create)


@router.get("/", tags=["users"], response_model=list[schemas.User])
async def get_users(session: AsyncSession = Depends(get_session)):
    users = await crud.users.get_all(session=session)
    logger.info("finished fetching users")
    return users


@router.get("/{user_id}", tags=["users"], response_model=schemas.User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await crud.users.get_one(session=session, user_id=user_id)
    if user is None:
        logger.error(f"tried to fetch a non existing user with id {user_id}")
        raise HTTPException(status_code=404, detail="User not found")
    return user
