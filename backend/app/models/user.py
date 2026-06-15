"""User Model"""
from sqlalchemy import Column, String, Boolean, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime
import enum
from app.db.database import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SUPERJUDGE = "superjudge"
    JUDGE = "judge"
    CANDIDATE = "candidate"

class ApprovalStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False, index=True)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.region_id", ondelete="SET NULL"), nullable=True, index=True)
    is_approved = Column(Enum(ApprovalStatus), default=ApprovalStatus.PENDING)
    is_active = Column(Boolean, default=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    region = relationship("Region")
    evaluations = relationship("Evaluation", back_populates="judge")
    audit_logs = relationship("AuditLog", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.full_name} ({self.role})>"
