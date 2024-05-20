from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import uvicorn

from db.database import SessionLocal
from schemas.user_schema import TeamCreate, UserCreate
import services.user_service as user_service

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

    
@app.get("/")
def root():
    return {"message" : "Hello, It's me"}

@app.get("/users")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip, limit)
    return users
    
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.create_user(db, user)
    return db_user

@app.get("/teams")
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return user_service.get_teams(db, skip, limit)

@app.post("/teams")
def create_teams(team: TeamCreate, db: Session = Depends(get_db)):
    db_team = user_service.create_team(db, team)
    return db_team

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
