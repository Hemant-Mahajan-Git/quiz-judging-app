"""User management routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.schemas.user import UserResponse
from app.crud.user import get_user_by_id, get_pending_judges, approve_judge, reject_judge
from app.core.deps import get_current_user, get_superjudge_user

router = APIRouter(prefix="/api/v1/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user = Depends(get_current_user)):
    """Get current authenticated user info"""
    return UserResponse.from_orm(current_user)

@router.get("/pending-judges", response_model=list[UserResponse])
def get_pending_judges_list(
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Get pending judges in the region (Superjudge only)"""
    judges = get_pending_judges(db, current_user.region_id)
    return [UserResponse.from_orm(j) for j in judges]

@router.post("/{user_id}/approve")
def approve_judge_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Approve a pending judge (Superjudge only)"""
    judge = approve_judge(db, user_id, current_user.region_id)
    return {"message": "Judge approved successfully", "user": UserResponse.from_orm(judge)}

@router.post("/{user_id}/reject")
def reject_judge_endpoint(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_superjudge_user)
):
    """Reject a pending judge (Superjudge only)"""
    judge = reject_judge(db, user_id, current_user.region_id)
    return {"message": "Judge rejected successfully", "user": UserResponse.from_orm(judge)}
