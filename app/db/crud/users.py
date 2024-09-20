from sqlalchemy.orm import Session, joinedload

from app.db import models, schemas


def get_one(db: Session, user_id: int, show_relation: bool = False) -> models.User:
    if show_relation:
        return db.query(models.User).filter(models.User.id == user_id).options(joinedload(models.User.articles)).first()
    else:
        return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_name(db: Session, name: str) -> models.User:
    return db.query(models.User).filter(models.User.name == name).first()


def get_all(db: Session) -> list[models.User]:
    return db.query(models.User).all()


def create(db: Session, user: schemas.UserCreate) -> models.User:
    user = models.User(name=user.name, email=user.email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
