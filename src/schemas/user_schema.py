from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    username: str = Field(min_length=8, max_length=32)
    firstname: str = Field(min_length=1, max_length=255)
    lastname: str = Field(min_length=1, max_length=255)
    email: EmailStr

class TeamCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
