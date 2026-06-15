"""User CRUD operations"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from uuid import UUID
from app.models.user import User, UserRole, ApprovalStatus
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password
from app.core.exceptions import EmailAlreadyExists, InvalidCredentials

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    # Check if email already exists in the region
    existing_user = db.query(User).filter(
        and_(
            User.email == user.email,
            User.region_id == user.region_id
        )
    ).first()
    
    if existing_user:
        raise EmailAlreadyExists()
    
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=get_password_hash(user.password),
        role=user.role,
        region_id=user.region_id,
        is_approved=ApprovalStatus.PENDING if user.role == UserRole.JUDGE else ApprovalStatus.APPROVED
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: UUID) -> User:
    """Get user by ID"""
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email_and_region(db: Session, email: str, region_id: UUID) -> User:
    """Get user by email and region"""
    return db.query(User).filter(
        and_(
            User.email == email,
            User.region_id == region_id
        )
    ).first()

def authenticate_user(db: Session, email: str, password: str, region_id: UUID) -> User:
    """Authenticate user with email and password"""
    user = get_user_by_email_and_region(db, email, region_id)
    
    if not user:
        raise InvalidCredentials()
    
    if not verify_password(password, user.password_hash):
        raise InvalidCredentials()
    
    if user.role == UserRole.JUDGE and user.is_approved != ApprovalStatus.APPROVED:
        from app.core.exceptions import UserNotApproved
        raise UserNotApproved()
    
    return user

def get_pending_judges(db: Session, region_id: UUID):
    """Get pending judges in a region"""
    return db.query(User).filter(
        and_(
            User.region_id == region_id,
            User.role == UserRole.JUDGE,
            User.is_approved == ApprovalStatus.PENDING
        )
    ).all()

def approve_judge(db: Session, user_id: UUID, region_id: UUID) -> User:
    """Approve a judge"""
    user = db.query(User).filter(
        and_(
            User.user_id == user_id,
            User.region_id == region_id,
            User.role == UserRole.JUDGE
        )
    ).first()
    
    if not user:
        from app.core.exceptions import NotFound
        raise NotFound("Judge")
    
    user.is_approved = ApprovalStatus.APPROVED
    db.commit()
    db.refresh(user)
    return user

def reject_judge(db: Session, user_id: UUID, region_id: UUID) -> User:
    """Reject a judge"""
    user = db.query(User).filter(
        and_(
            User.user_id == user_id,
            User.region_id == region_id,
            User.role == UserRole.JUDGE
        )
    ).first()
    
    if not user:
        from app.core.exceptions import NotFound
        raise NotFound("Judge")
    
    user.is_approved = ApprovalStatus.REJECTED
    db.commit()
    db.refresh(user)
    return user
