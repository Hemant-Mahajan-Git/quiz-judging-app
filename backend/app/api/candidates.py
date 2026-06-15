"""Candidate management routes"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.schemas.candidate import CandidateCreate, CandidateResponse, CandidateDetailResponse, CandidateUpdate
from app.crud.candidate import (
    create_candidate, get_candidate_by_id, get_candidates_by_region,
    get_candidates_count, update_candidate, delete_candidate
)
from app.core.deps import get_current_user, get_superjudge_user
from app.models.user import UserRole

router = APIRouter(prefix="/api/v1/candidates", tags=["Candidates"])

@router.get("", response_model=dict)
def get_candidates(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get all candidates in user's region"""
    candidates = get_candidates_by_region(db, current_user.region_id, skip, limit)
    total = get_candidates_count(db, current_user.region_id)
    
    return {
        "data": candidates,
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": total
        }
    }

@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
def create_new_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Create a new candidate (Superjudge only)"""
    db_candidate = create_candidate(db, candidate, current_user.region_id)
    return db_candidate

@router.get("/{candidate_id}", response_model=CandidateDetailResponse)
def get_candidate(
    candidate_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Get candidate details"""
    candidate = get_candidate_by_id(db, candidate_id, current_user.region_id)
    if not candidate:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return candidate

@router.put("/{candidate_id}", response_model=CandidateResponse)
def update_candidate_endpoint(
    candidate_id: UUID,
    candidate_update: CandidateUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Update candidate (Superjudge only)"""
    updated = update_candidate(db, candidate_id, current_user.region_id, candidate_update)
    return updated

@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_candidate_endpoint(
    candidate_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Delete candidate (Superjudge only)"""
    delete_candidate(db, candidate_id, current_user.region_id)
    return None
