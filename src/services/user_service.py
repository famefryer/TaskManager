from sqlalchemy.orm import Session

from models.user_model import User
from schemas.user_schema import UserCreateRequest
import repos.user_repo as user_repo

def get_users(db: Session, skip: int, limit: int) -> list[User]:
    return user_repo.get_all_users(db, skip, limit)

def get_user_by_id(db: Session, user_id: str) -> User:
    return user_repo.find_user_by_id(db, user_id)

def get_user_by_username(db:Session, username: str) -> User:
    return user_repo.find_user_by_username(db, username)
    
def create_user(db: Session, user: UserCreateRequest) -> User:
    if user_repo.find_user_by_username(db, user.username) is not None:
        raise ValueError('Error username already exists')
    
    db_user = user_repo.create_user(db, user)
    return db_user

def delete_user_by_id(db:Session, id: str):
    db_user = user_repo.find_user_by_id(db, id)
    if db_user is None:
        raise ValueError('Error user does not exist')
    
    user_repo.delete_user(db, db_user)
    
def delete_user_by_username(db:Session, username: str):
    db_user = user_repo.find_user_by_username(db, username)
    if db_user is None:
        raise ValueError('Error user does not exist')
    
    user_repo.delete_user(db, db_user)
    
def clear_all_deleted_user(db: Session) -> int:
    res = user_repo.delete_all_soft_deleted_users(db)
    return res
