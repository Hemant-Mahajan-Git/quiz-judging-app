"""Evaluation schemas"""
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

class EvaluationBase(BaseModel):
    scores_criteria: Dict[str, Any] = Field(default_factory=dict)
    total_score: Decimal = Field(..., ge=0, le=100, decimal_places=2)
    comments: Optional[str] = None

class EvaluationCreate(BaseModel):
    candidate_id: UUID
    scores_criteria: Dict[str, Any] = Field(default_factory=dict)
    total_score: Decimal = Field(..., ge=0, le=100, decimal_places=2)
    comments: Optional[str] = None

class EvaluationUpdate(BaseModel):
    scores_criteria: Optional[Dict[str, Any]] = None
    total_score: Optional[Decimal] = Field(None, ge=0, le=100, decimal_places=2)
    comments: Optional[str] = None

class EvaluationResponse(EvaluationBase):
    evaluation_id: UUID
    candidate_id: UUID
    judge_id: UUID
    region_id: UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
