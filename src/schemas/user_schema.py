from pydantic import BaseModel, Field, EmailStr, UUID4
from datetime import datetime

# Request Model
class UserCreateRequest(BaseModel):
    username: str = Field(min_length=8, max_length=32)
    firstname: str = Field(min_length=1, max_length=255)
    lastname: str = Field(min_length=1, max_length=255)
    email: EmailStr

class LoginRequest(BaseModel):
    username: str = Field(min_length=8, max_length=32)

class TeamCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)

class TeamMemberAddRequest(BaseModel):
    user_id: str = Field(min_length=36, max_length=36)

class TeamMemberRemoveRequest(BaseModel):
    user_id: str = Field(min_length=36, max_length=36)

# Response Model
class UserTeam(BaseModel):
    id: UUID4
    name: str

class UserResponse(BaseModel):
    id: UUID4
    username: str
    firstname: str
    lastname: str
    email: EmailStr
    created_at: datetime
    last_updated_at: datetime
    teams: list[UserTeam]
    
    class Config:
        from_attributes = True


class TeamUser(BaseModel):
    id: UUID4
    username: str
    
class TeamResponse(BaseModel):
    id: UUID4
    name: str
    created_at: datetime
    last_updated_at: datetime
    members: list[TeamUser]
    
    class Config:
        from_attributes = True
