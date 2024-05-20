from sqlalchemy.orm import Session

from models.user_model import User
from schemas.user_schema import UserCreateRequest

def get_all_users(db: Session, skip: int, limit: int):
    return db.query(User).offset(skip).limit(limit).all()

def find_user_by_id(db: Session, id: int):
    return db.query(User).where(User.id == id).first()

def find_user_by_username(db: Session, username: str):
    return db.query(User).where(User.username == username).first()

def create_user(db: Session, user: UserCreateRequest):
    db_user = User(username=user.username, firstname=user.firstname, lastname=user.lastname, email=user.email)
    db.add(db_user)
    db.commit()
    return db_user
