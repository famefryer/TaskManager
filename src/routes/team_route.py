from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from dependencies import get_db
from schemas.user_schema import TeamCreateRequest, TeamMemberAddRequest, TeamResponse
from services import team_service

team_router = APIRouter()

@team_router.get("", response_model=list[TeamResponse])
def get_all_teams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return team_service.get_teams(db, skip, limit)

@team_router.get("/{team_id}", response_model=TeamResponse)
def get_team_by_id(team_id: str, db: Session = Depends(get_db)):
    team = team_service.get_team_by_id(db, team_id)
    if team is None:
        raise HTTPException(status_code='404', detail='Team not found')

    return team

@team_router.get("/by-name/{team_name}", response_model=TeamResponse)
def get_team_by_name(team_name: str, db: Session = Depends(get_db)):
    team = team_service.get_team_by_name(db, team_name)
    if team is None:
        raise HTTPException(status_code='404', detail='Team not found')

    return team

@team_router.post("", response_model=TeamResponse)
def create_team(team: TeamCreateRequest, db: Session = Depends(get_db)):
    db_team = team_service.create_team(db, team)
    return db_team

@team_router.post("/{team_id}/add-member", response_model=TeamResponse)
def add_team_member(team_id: str, team_member: TeamMemberAddRequest, db: Session = Depends(get_db)):
    res = team_service.add_team_member(db, team_id, team_member)
    return res

@team_router.post("/{team_id}/remove-member", response_model=TeamResponse)
def add_team_member(team_id: str, team_member: TeamMemberAddRequest, db: Session = Depends(get_db)):
    res = team_service.remove_team_member(db, team_id, team_member)
    return res

@team_router.delete("")
def delete_team(team_id: str = None, team_name: str = None, db: Session = Depends(get_db)):
    if team_id is None and team_name is None:
        raise HTTPException(status_code='400', detail='Both team_id and team_name are None')

    if team_id is not None:
        team_service.delete_team_by_id(db, team_id)
    elif team_name is not None:
        team_service.delete_team_by_name(db, team_name)
    
    return { "status" : "success"}

@team_router.post("/clear-deleted-teams")
def clear_all_deleted_teams(db: Session = Depends(get_db)):
    num = team_service.clear_all_deleted_team(db)
    
    return { "deleted_items": num}
