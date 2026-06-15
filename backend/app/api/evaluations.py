"""Evaluation routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime
from app.db.database import get_db
from app.schemas.evaluation import EvaluationCreate, EvaluationResponse, EvaluationUpdate
from app.crud.evaluation import (
    create_evaluation, get_evaluation_by_id, get_evaluations_by_judge,
    get_evaluations_by_candidate, get_region_evaluation_summary, update_evaluation
)
from app.core.deps import get_current_user, get_superjudge_user
from app.models.user import UserRole

router = APIRouter(prefix="/api/v1/evaluations", tags=["Evaluations"])

@router.post("", response_model=EvaluationResponse, status_code=status.HTTP_201_CREATED)
def submit_evaluation(
    evaluation: EvaluationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Submit an evaluation (Judge only)"""
    if current_user.role != UserRole.JUDGE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only judges can submit evaluations")
    
    db_evaluation = create_evaluation(db, evaluation, current_user.user_id, current_user.region_id)
    return db_evaluation

@router.get("", response_model=dict)
def get_evaluations(
    candidate_id: UUID = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get evaluations for current user"""
    evaluations = get_evaluations_by_judge(db, current_user.user_id, current_user.region_id, skip, limit)
    return {"data": evaluations}

@router.get("/region/summary")
def get_region_summary(
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Get evaluation summary for region (Superjudge only)"""
    summary = get_region_evaluation_summary(db, current_user.region_id)
    return summary

@router.get("/candidate/{candidate_id}", response_model=dict)
def get_candidate_evaluations(
    candidate_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all evaluations for a candidate"""
    evaluations = get_evaluations_by_candidate(db, candidate_id, current_user.region_id)
    return {"data": evaluations}

@router.put("/{evaluation_id}", response_model=EvaluationResponse)
def update_evaluation_endpoint(
    evaluation_id: UUID,
    evaluation_update: EvaluationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Update an evaluation"""
    updated = update_evaluation(db, evaluation_id, current_user.region_id, evaluation_update)
    return updated
