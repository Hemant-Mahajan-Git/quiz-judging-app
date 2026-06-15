"""Authentication routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, TokenResponse, UserResponse
from app.crud.user import create_user, authenticate_user
from app.core.security import create_access_token
from app.config import settings

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (Judge, Superjudge, Candidate)"""
    db_user = create_user(db, user)
    return db_user

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT token"""
    user = authenticate_user(db, credentials.email, credentials.password, credentials.region_id)
    
    # Create JWT token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.user_id), "region_id": str(user.region_id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse.from_orm(user),
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
