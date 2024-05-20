from sqlalchemy.orm import Session

from schemas.user_schema import UserCreateRequest
import repos.user_repo as user_repo

def get_users(db: Session, skip: int, limit: int):
    return user_repo.get_all_users(db, skip, limit)

def get_user_by_id(db: Session, user_id: str):
    return user_repo.find_user_by_id(db, user_id)

def get_user_by_username(db:Session, username: str):
    return user_repo.find_user_by_username(db, username)
    
def create_user(db: Session, user: UserCreateRequest):
    if user_repo.find_user_by_username(db, user.username) is not None:
        raise ValueError('Error username already exists')
    
    db_user = user_repo.create_user(db, user)
    return db_user
