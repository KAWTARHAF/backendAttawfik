from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime

UserRole = Literal['admin', 'manager', 'leader', 'user']

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = 'user'
    department_id: Optional[int] = None

class UserCreate(UserBase):
    password: str = Field(min_length=6)

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[UserRole] = None
    department_id: Optional[int] = None
    password: Optional[str] = Field(default=None, min_length=6)

class UserResponse(UserBase):
    id: int
    created_at: datetime