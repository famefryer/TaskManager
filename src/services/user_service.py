from sqlalchemy.orm import Session

from models.user_model import Team, User
from schemas.user_schema import TeamCreate, UserCreate

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username, firstname=user.firstname, lastname=user.lastname, email=user.email)
    db.add(db_user)
    db.commit()
    return db_user

def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Team).offset(skip).limit(limit).all()

def create_team(db: Session, team: TeamCreate):
    db_team = Team(name=team.name)
    db.add(db_team)
    db.commit()
    return db_team
    