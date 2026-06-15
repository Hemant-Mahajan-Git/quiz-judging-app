"""Evaluation Model"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Numeric, UniqueConstraint, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.db.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"
    __table_args__ = (
        UniqueConstraint("candidate_id", "judge_id", "region_id", name="unique_judge_candidate_region"),
    )
    
    evaluation_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    candidate_id = Column(UUID(as_uuid=True), ForeignKey("candidates.candidate_id", ondelete="CASCADE"), nullable=False, index=True)
    judge_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.region_id", ondelete="CASCADE"), nullable=False, index=True)
    
    scores_criteria = Column(JSON, default={})
    total_score = Column(Numeric(5, 2), nullable=False)
    comments = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    candidate = relationship("Candidate", back_populates="evaluations")
    judge = relationship("User", back_populates="evaluations")
    region = relationship("Region")
    
    def __repr__(self):
        return f"<Evaluation {self.candidate_id} by {self.judge_id}>"

class EvaluationCriteria(Base):
    __tablename__ = "evaluation_criteria"
    __table_args__ = (
        UniqueConstraint("region_id", "name", name="criteria_name_region_unique"),
    )
    
    criteria_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.region_id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    max_score = Column(Numeric(5, 2), default=100)
    weight = Column(Numeric(3, 2), default=1.0)
    is_active = Column(String(10), default="true")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    region = relationship("Region")
    
    def __repr__(self):
        return f"<EvaluationCriteria {self.name}>"
