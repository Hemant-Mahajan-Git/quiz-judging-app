"""Candidate Model"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
from app.db.database import Base

class Candidate(Base):
    __tablename__ = "candidates"
    
    candidate_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    candidate_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    registration_number = Column(String(100), nullable=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.region_id", ondelete="CASCADE"), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(String(50), default="active", index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    region = relationship("Region")
    evaluations = relationship("Evaluation", back_populates="candidate", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Candidate {self.candidate_name}>"
