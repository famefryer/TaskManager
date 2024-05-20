from typing import Optional
from pydantic import BaseModel, Field, EmailStr, UUID4, field_serializer
from datetime import datetime

from models.task_model import TaskPermissionLevel, TaskPermissionType, TaskStatus

class User(BaseModel):
    user_id: UUID4
    username: str

class TaskBase(BaseModel):
    id: UUID4
    version: int
    topic: str
    description: str
    status: TaskStatus
    assignee: Optional[UUID4] = None
    use_permission: bool
    
    @field_serializer('status')
    def get_status_value(self, v) -> str:
        return str(TaskStatus(v).name)

class Permission(BaseModel):
    entity_id: str
    permission_level: TaskPermissionLevel
    
class PermissionForm(BaseModel):
    user_permissions: list[Permission] = []
    team_permissions: list[Permission] = []

# Request Model
class TaskCreateRequest(BaseModel):
    topic: str
    description: str
    assignee_id: str = None
    permissions: PermissionForm = None

class TaskEditRequest(BaseModel):
    topic: str = None
    description: str = None
    status: TaskStatus = None
    assignee_id: str = None
    
class TaskUndoRequest(BaseModel):
    undo_depth: int

# Response Model
class TaskResponse(TaskBase):
    created_by: UUID4
    created_at: datetime
    last_updated_at: datetime
    
    class Config:
        from_attributes = True
        
class TaskHistoryResponse(TaskBase):
    task_id: UUID4
    edited_by: UUID4
    edited_at: datetime
    
    class Config:
        from_attributes = True
