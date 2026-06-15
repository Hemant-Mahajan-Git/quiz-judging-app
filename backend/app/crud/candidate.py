"""Candidate CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from uuid import UUID
from app.models.candidate import Candidate
from app.models.evaluation import Evaluation
from app.schemas.candidate import CandidateCreate, CandidateUpdate
from app.core.exceptions import NotFound, RegionIsolationError

def create_candidate(db: Session, candidate: CandidateCreate, region_id: UUID) -> Candidate:
    """Create a new candidate in a region"""
    db_candidate = Candidate(
        candidate_name=candidate.candidate_name,
        email=candidate.email,
        phone=candidate.phone,
        registration_number=candidate.registration_number,
        description=candidate.description,
        region_id=region_id
    )
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def get_candidate_by_id(db: Session, candidate_id: UUID, region_id: UUID = None) -> Candidate:
    """Get candidate by ID"""
    query = db.query(Candidate).filter(Candidate.candidate_id == candidate_id)
    
    if region_id:
        query = query.filter(Candidate.region_id == region_id)
    
    candidate = query.first()
    return candidate

def get_candidates_by_region(db: Session, region_id: UUID, skip: int = 0, limit: int = 10):
    """Get candidates in a region"""
    candidates = db.query(Candidate).filter(
        Candidate.region_id == region_id
    ).offset(skip).limit(limit).all()
    
    # Add evaluation count and average score
    for candidate in candidates:
        eval_stats = db.query(
            func.count(Evaluation.evaluation_id).label('count'),
            func.avg(Evaluation.total_score).label('avg_score')
        ).filter(
            Evaluation.candidate_id == candidate.candidate_id
        ).first()
        
        candidate.evaluation_count = eval_stats.count or 0
        candidate.average_score = eval_stats.avg_score
    
    return candidates

def get_candidates_count(db: Session, region_id: UUID) -> int:
    """Get total count of candidates in region"""
    return db.query(Candidate).filter(Candidate.region_id == region_id).count()

def update_candidate(db: Session, candidate_id: UUID, region_id: UUID, candidate_update: CandidateUpdate) -> Candidate:
    """Update a candidate"""
    db_candidate = get_candidate_by_id(db, candidate_id, region_id)
    
    if not db_candidate:
        raise NotFound("Candidate")
    
    if db_candidate.region_id != region_id:
        raise RegionIsolationError()
    
    for key, value in candidate_update.dict(exclude_unset=True).items():
        setattr(db_candidate, key, value)
    
    db.commit()
    db.refresh(db_candidate)
    return db_candidate

def delete_candidate(db: Session, candidate_id: UUID, region_id: UUID) -> bool:
    """Delete a candidate"""
    db_candidate = get_candidate_by_id(db, candidate_id, region_id)
    
    if not db_candidate:
        raise NotFound("Candidate")
    
    if db_candidate.region_id != region_id:
        raise RegionIsolationError()
    
    db.delete(db_candidate)
    db.commit()
    return True
