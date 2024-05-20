from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import uvicorn

from db.database import SessionLocal
from schemas.user_schema import TeamCreateRequest, TeamMemberAddRequest, TeamResponse, UserResponse, UserCreateRequest
import services.user_service as user_service
import services.team_service as team_service

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

@app.get("/users", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_service.get_users(db, skip, limit)
    return users
    
@app.post("/users", response_model=UserResponse)
def create_user(user: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = user_service.create_user(db, user)
    return db_user

@app.get("/teams", response_model=list[TeamResponse])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return team_service.get_teams(db, skip, limit)

@app.post("/teams", response_model=TeamResponse)
def create_team(team: TeamCreateRequest, db: Session = Depends(get_db)):
    db_team = team_service.create_team(db, team)
    return db_team

@app.post("/teams/{team_id}", response_model=TeamResponse)
def add_team_member(team_id: str, team_member: TeamMemberAddRequest, db: Session = Depends(get_db)):
    res = team_service.add_team_member(db, team_id, team_member)
    return res

if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
