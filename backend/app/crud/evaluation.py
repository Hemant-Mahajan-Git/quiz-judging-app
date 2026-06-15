"""Evaluation CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from uuid import UUID
from app.models.evaluation import Evaluation
from app.models.candidate import Candidate
from app.schemas.evaluation import EvaluationCreate, EvaluationUpdate
from app.core.exceptions import NotFound, RegionIsolationError

def create_evaluation(db: Session, evaluation: EvaluationCreate, judge_id: UUID, region_id: UUID) -> Evaluation:
    """Create a new evaluation"""
    # Verify candidate exists in the region
    candidate = db.query(Candidate).filter(
        and_(
            Candidate.candidate_id == evaluation.candidate_id,
            Candidate.region_id == region_id
        )
    ).first()
    
    if not candidate:
        raise NotFound("Candidate")
    
    # Check if judge has already evaluated this candidate
    existing = db.query(Evaluation).filter(
        and_(
            Evaluation.candidate_id == evaluation.candidate_id,
            Evaluation.judge_id == judge_id,
            Evaluation.region_id == region_id
        )
    ).first()
    
    if existing:
        # Update existing evaluation
        existing.scores_criteria = evaluation.scores_criteria
        existing.total_score = evaluation.total_score
        existing.comments = evaluation.comments
        db.commit()
        db.refresh(existing)
        return existing
    
    db_evaluation = Evaluation(
        candidate_id=evaluation.candidate_id,
        judge_id=judge_id,
        region_id=region_id,
        scores_criteria=evaluation.scores_criteria,
        total_score=evaluation.total_score,
        comments=evaluation.comments
    )
    
    db.add(db_evaluation)
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation

def get_evaluation_by_id(db: Session, evaluation_id: UUID, region_id: UUID = None) -> Evaluation:
    """Get evaluation by ID"""
    query = db.query(Evaluation).filter(Evaluation.evaluation_id == evaluation_id)
    
    if region_id:
        query = query.filter(Evaluation.region_id == region_id)
    
    return query.first()

def get_evaluations_by_judge(db: Session, judge_id: UUID, region_id: UUID, skip: int = 0, limit: int = 10):
    """Get evaluations by judge in region"""
    return db.query(Evaluation).filter(
        and_(
            Evaluation.judge_id == judge_id,
            Evaluation.region_id == region_id
        )
    ).offset(skip).limit(limit).all()

def get_evaluations_by_candidate(db: Session, candidate_id: UUID, region_id: UUID):
    """Get all evaluations for a candidate"""
    return db.query(Evaluation).filter(
        and_(
            Evaluation.candidate_id == candidate_id,
            Evaluation.region_id == region_id
        )
    ).all()

def get_region_evaluation_summary(db: Session, region_id: UUID):
    """Get evaluation summary for a region"""
    summary = db.query(
        func.count(Evaluation.evaluation_id).label('total_evaluations'),
        func.count(func.distinct(Evaluation.judge_id)).label('total_judges'),
        func.count(func.distinct(Evaluation.candidate_id)).label('total_candidates'),
        func.avg(Evaluation.total_score).label('average_score'),
        func.max(Evaluation.total_score).label('highest_score'),
        func.min(Evaluation.total_score).label('lowest_score')
    ).filter(
        Evaluation.region_id == region_id
    ).first()
    
    return {
        'total_evaluations': summary.total_evaluations or 0,
        'total_judges': summary.total_judges or 0,
        'total_candidates': summary.total_candidates or 0,
        'average_score': float(summary.average_score) if summary.average_score else 0,
        'highest_score': float(summary.highest_score) if summary.highest_score else 0,
        'lowest_score': float(summary.lowest_score) if summary.lowest_score else 0
    }

def update_evaluation(db: Session, evaluation_id: UUID, region_id: UUID, evaluation_update: EvaluationUpdate) -> Evaluation:
    """Update an evaluation"""
    db_evaluation = get_evaluation_by_id(db, evaluation_id, region_id)
    
    if not db_evaluation:
        raise NotFound("Evaluation")
    
    if db_evaluation.region_id != region_id:
        raise RegionIsolationError()
    
    for key, value in evaluation_update.dict(exclude_unset=True).items():
        setattr(db_evaluation, key, value)
    
    db.commit()
    db.refresh(db_evaluation)
    return db_evaluation
