"""User schemas"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional
from app.models.user import UserRole, ApprovalStatus

class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255, description="Full name of the user")
    email: EmailStr
    role: UserRole
    region_id: Optional[UUID] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    region_id: UUID

class UserResponse(UserBase):
    user_id: UUID
    is_approved: ApprovalStatus
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
    expires_in: int
