from db.database import Base
from sqlalchemy import UUID, Column, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class User(Base):
    __tablename__ = 'user'
    
    id = Column(UUID, primary_key=True)
    permission_entity_id = Column(String, nullable=False)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    email = Column(String, nullable=True)
    created_at = Column(DateTime, default= func.now(), nullable=False)
    last_updated_at = Column(DateTime, default= func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    teams = relationship('Team', secondary='team_member', secondaryjoin='and_(team_member.c.team_id == Team.id, Team.deleted_at == None)', back_populates='members')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
        self.permission_entity_id = f'U-{self.id}'

class Team(Base):
    __tablename__ = 'team'
    
    id = Column(UUID, primary_key=True)
    permission_entity_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default= func.now(), nullable=False)
    last_updated_at = Column(DateTime, default= func.now(), onupdate=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)

    members = relationship('User', secondary='team_member', secondaryjoin='and_(team_member.c.user_id == User.id, User.deleted_at == None)', back_populates='teams')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
        self.permission_entity_id = f'T-{self.id}'


class TeamMember(Base):
    __tablename__ = 'team_member'
    
    id = Column('id', UUID, primary_key=True)
    team_id = Column('team_id', UUID, ForeignKey('team.id', ondelete='CASCADE'), nullable=False)
    user_id = Column('user_id', UUID, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
