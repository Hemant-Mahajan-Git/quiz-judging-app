"""Candidate schemas"""
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, List
from decimal import Decimal

class CandidateBase(BaseModel):
    candidate_name: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    registration_number: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class CandidateCreate(CandidateBase):
    pass

class CandidateUpdate(BaseModel):
    candidate_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = None

class CandidateResponse(CandidateBase):
    candidate_id: UUID
    region_id: UUID
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CandidateDetailResponse(CandidateResponse):
    evaluation_count: int = 0
    average_score: Optional[Decimal] = None
