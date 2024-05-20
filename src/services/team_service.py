from sqlalchemy.orm import Session

from models.user_model import Team
from schemas.user_schema import TeamCreateRequest, TeamMemberAddRequest, TeamMemberRemoveRequest
import repos.team_repo as team_repo
import repos.user_repo as user_repo

def get_teams(db: Session, skip: int = 0, limit: int = 100) -> list[Team]:
    return team_repo.get_all_teams(db, skip, limit)

def create_team(db: Session, team: TeamCreateRequest) -> Team:
    if team_repo.find_team_by_name(db, team.name) is not None:
        raise ValueError('Error team name already exists')

    return team_repo.create_team(db, team)

def get_team_by_id(db: Session, team_id: str) -> Team:
    return team_repo.find_team_by_id(db, team_id)

def get_team_by_name(db:Session, name: str) -> Team:
    return team_repo.find_team_by_name(db, name)

def add_team_member(db: Session, team_id: str, team_member: TeamMemberAddRequest) -> Team:
    db_user = user_repo.find_user_by_id(db, team_member.user_id)
    db_team = team_repo.find_team_by_id(db, team_id)
    
    if db_user is None or db_team is None:
        # TODO Add custom exception
        raise ValueError('User or Team doesn\'t exist')
    
    db_cur_team_member = team_repo.find_team_member(db, team_id, team_member.user_id)
    if db_cur_team_member is not None:
        # TODO Add custom exception
        raise ValueError('User already in the team')

    team_repo.add_user_to_team(db, db_team, team_member.user_id)
    return db_team

def remove_team_member(db: Session, team_id: str, team_member: TeamMemberRemoveRequest) -> Team:   
    db_team_member = team_repo.find_team_member(db, team_id, team_member.user_id)
    if db_team_member is None:
        # TODO Add custom exception
        raise ValueError('User is not in the team')

    team_repo.remove_user_from_team(db, db_team_member)
    return team_repo.find_team_by_id(db, team_id)

def delete_team_by_id(db:Session, id: str):
    db_team = team_repo.find_team_by_id(db, id)
    if db_team is None:
        raise ValueError('Error team does not exist')
    
    team_repo.delete_team(db, db_team)
    
def delete_team_by_name(db:Session, name: str):
    db_team = team_repo.find_team_by_name(db, name)
    if db_team is None:
        raise ValueError('Error team does not exist')
    
    team_repo.delete_team(db, db_team)
    
def clear_all_deleted_team(db: Session) -> int:
    res = team_repo.delete_all_soft_deleted_teams(db)
    return res
