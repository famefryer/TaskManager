from db.database import Base
from sqlalchemy import UUID, Column, DateTime, String, ForeignKey, Integer, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum

import uuid

class TaskStatus(Enum):
    OPEN = 'OPEN'
    IN_PROGRESS = 'IN_PROGRESS'
    DONE = 'DONE'
    CANCELLED = 'CANCELLED'
    DELETED = 'DELETED'
    
class TaskPermissionLevel(Enum):
    VIEW = 'VIEW'
    EDIT = 'EDIT'
    DELETE = 'DELETE'
    
class TaskPermissionType(Enum):
    USER = 'USER'
    TEAM = 'TEAM'

class Task(Base):
    __tablename__ = 'task'
    
    id = Column(UUID, primary_key=True)
    version = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(TaskStatus), nullable=False)
    created_by = Column(UUID, ForeignKey('user.id'), nullable=False)
    assignee = Column(UUID, ForeignKey('user.id'), nullable=True)
    use_permission = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(), default= func.now(), nullable=False)
    last_updated_at = Column(DateTime(), default= func.now(), nullable=False)
    deleted_at = Column(DateTime(), nullable=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
        self.version = 1
        self.status = TaskStatus.OPEN

class TaskHistory(Base):
    __tablename__ = 'task_history'
    
    id = Column(UUID, primary_key=True)
    task_id = Column(UUID, nullable=False)
    version = Column(Integer, nullable=False)
    topic = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SQLEnum(TaskStatus), nullable=False)
    assignee = Column(UUID, ForeignKey('user.id'), nullable=True)
    use_permission = Column(Boolean, default=False, nullable=False)
    edited_by = Column(UUID, ForeignKey('user.id'), nullable=False)
    edited_at = Column(DateTime(), default= func.now(), nullable=False)
    deleted_at = Column(DateTime(), nullable=True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()

class TaskPermission(Base):
    __tablename__ = 'task_permission'
    
    id = Column(UUID, primary_key=True)
    task_id = Column(UUID, ForeignKey('task.id'), nullable=False)
    permission_entity_id = Column('permission_entity_id', String, nullable=False)
    permission_type = Column('permission_type', SQLEnum(TaskPermissionType), nullable=False)
    permission_level = Column('permissionLevel', SQLEnum(TaskPermissionLevel), nullable=False)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id = uuid.uuid4()
