from sqlalchemy import func
from sqlalchemy.orm import Session

from models.user_model import Team, TeamMember
from schemas.user_schema import TeamCreateRequest


def get_all_teams(db: Session, skip: int, limit: int) -> list[Team]:
    return db.query(Team).where(Team.deleted_at == None).offset(skip).limit(limit).all()


def find_team_by_id(db: Session, id: int) -> Team:
    return db.query(Team).where(Team.deleted_at == None).where(Team.id == id).first()


# def find_team_by_permission_entity_id(db: Session, permission_entity_id: int):
#     return db.query(Team).where(Team.deleted_at == None).where(Team.permission_entity_id == permission_entity_id).first()


def find_team_by_name(db: Session, name: str) -> Team:
    return (
        db.query(Team).where(Team.deleted_at == None).where(Team.name == name).first()
    )


def find_team_member(db: Session, team_id: str, user_id: str) -> TeamMember:
    return (
        db.query(TeamMember)
        .where(TeamMember.team_id == team_id)
        .where(TeamMember.user_id == user_id)
        .first()
    )


def create_team(db: Session, team: TeamCreateRequest) -> Team:
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    return db_team


def delete_team(db: Session, team: Team):
    team.deleted_at = func.now()
    db.commit()


def delete_all_soft_deleted_teams(db: Session) -> int:
    res = db.query(Team).filter(Team.deleted_at != None).delete()
    db.commit()
    return res


def add_user_to_team(db: Session, db_team: Team, user_id: str) -> TeamMember:
    db_team_member = TeamMember(user_id=user_id, team_id=db_team.id)
    db.add(db_team_member)
    db.commit()
    db.refresh(db_team)

    return db_team_member


def remove_user_from_team(db: Session, db_team_member: TeamMember) -> None:
    db.delete(db_team_member)
    db.commit()
