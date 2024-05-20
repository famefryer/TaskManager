from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from dependencies import get_db
from exceptions.custom_exception import EntityNotFoundException
from schemas.user_schema import LoginRequest, UserCreateRequest, UserResponse 
from services import user_service

user_router = APIRouter()

@user_router.get("", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip, limit)
    return users
    
@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_userid(user_id: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise EntityNotFoundException('User', user_id)

    return user

@user_router.post("/login", response_model=UserResponse)
def login(login_req: LoginRequest, db: Session = Depends(get_db)):
    user = user_service.get_user_by_username(db, login_req.username)
    if user is None:
        raise EntityNotFoundException('User', login_req.username, col_name='username')

    return user

@user_router.post("", response_model=UserResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = user_service.create_user(db, user)
    return db_user

@user_router.delete("")
def delete_user(id: str = None, username: str = None, db: Session = Depends(get_db)):
    if id is None and username is None:
        raise HTTPException(status_code='400', detail='Both id and username are None')

    if id is not None:
        user_service.delete_user_by_id(db, id)
    elif username is not None:
        user_service.delete_user_by_username(db, username)
    
    return { "status" : "success"}

@user_router.post("/clear-deleted-users")
def clear_all_deleted_users(db: Session = Depends(get_db)):
    num = user_service.clear_all_deleted_user(db)
    
    return { "deleted_items": num}
