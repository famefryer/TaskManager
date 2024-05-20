from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.user_schema import TeamCreateRequest, TeamMemberAddRequest, TeamResponse
from services import team_service

team_router = APIRouter()

@team_router.get("", response_model=list[TeamResponse])
def read_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return team_service.get_teams(db, skip, limit)

@team_router.post("", response_model=TeamResponse)
def create_team(team: TeamCreateRequest, db: Session = Depends(get_db)):
    db_team = team_service.create_team(db, team)
    return db_team

@team_router.post("/{team_id}", response_model=TeamResponse)
def add_team_member(team_id: str, team_member: TeamMemberAddRequest, db: Session = Depends(get_db)):
    res = team_service.add_team_member(db, team_id, team_member)
    return res
