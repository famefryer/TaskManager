from sqlalchemy.orm import Session

from models.user_model import Team, TeamMember
from schemas.user_schema import TeamCreateRequest

def get_all_teams(db: Session, skip: int, limit: int):
    return db.query(Team).offset(skip).limit(limit).all()

def find_team_by_id(db: Session, id: int):
    return db.query(Team).where(Team.id == id).first()

def find_team_by_name(db: Session, name: str):
    return db.query(Team).where(Team.name == name).first()

def find_team_member(db: Session, team_id: str, user_id: str):
    return db.query(TeamMember).where(TeamMember.team_id==team_id).where(TeamMember.user_id==user_id).first()

def create_team(db: Session, team: TeamCreateRequest):
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    return db_team

def add_user_to_team(db: Session, db_team: Team, user_id: str):
    db_team_member = TeamMember(user_id=user_id, team_id=db_team.id)
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team)

    return db_team
