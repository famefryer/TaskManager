from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.user_schema import UserCreateRequest, UserResponse 
from services import user_service

user_router = APIRouter()

@user_router.get("", response_model=list[UserResponse])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip, limit)
    return users

@user_router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code='404', detail='User not found')

    return user
    
@user_router.get("/", response_model=UserResponse)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = user_service.get_user_by_username(db, username)
    if user is None:
        raise HTTPException(status_code='404', detail='User not found')

    return user

@user_router.post("", response_model=UserResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = user_service.create_user(db, user)
    return db_user
