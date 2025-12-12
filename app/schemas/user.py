# app/schemas/user.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=128)

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic v2; for v1 use orm_mode = True

class UserLogin(BaseModel):
    # Allow extra fields (like username) so old tests don't break
    model_config = ConfigDict(extra="ignore")

    email: EmailStr
    password: str
    
class UserUpdate(BaseModel):
    """Fields user is allowed to update on their profile."""
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class PasswordChange(BaseModel):
    old_password: str
    new_password: str
