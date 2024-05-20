from sqlalchemy import func
from sqlalchemy.orm import Session

from models.user_model import User
from schemas.user_schema import UserCreateRequest


def get_all_users(db: Session, skip: int, limit: int) -> User:
    return db.query(User).where(User.deleted_at == None).offset(skip).limit(limit).all()


def find_user_by_id(db: Session, id: int) -> User:
    return db.query(User).where(User.deleted_at == None).where(User.id == id).first()


def find_user_by_permission_entity_id(db: Session, permission_entity_id: int) -> User:
    return (
        db.query(User)
        .where(User.deleted_at == None)
        .where(User.permission_entity_id == permission_entity_id)
        .first()
    )


def find_user_by_username(db: Session, username: str) -> User:
    return (
        db.query(User)
        .where(User.deleted_at == None)
        .where(User.username == username)
        .first()
    )


def create_user(db: Session, user: UserCreateRequest) -> User:
    db_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
    )
    db.add(db_user)
    db.commit()
    return db_user


def delete_user(db: Session, user: User):
    user.deleted_at = func.now()
    db.commit()


def delete_all_soft_deleted_users(db: Session) -> int:
    res = db.query(User).filter(User.deleted_at != None).delete()
    db.commit()
    return res
