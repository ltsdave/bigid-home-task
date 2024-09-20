from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import schemas
from app.db import crud
from app.db.database import get_db

router = APIRouter(prefix="/users")


@router.post("/", tags=["users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.users.get_by_name(db=db, user=user.name)
    if user:
        raise HTTPException(status_code=400, detail="User already registered")
    return crud.users.create(db=db, user=user)


@router.get("/", tags=["users"], response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = crud.users.get_all(db=db)
    return users


@router.get("/{user_id}", tags=["users"], response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.users.get_one(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
