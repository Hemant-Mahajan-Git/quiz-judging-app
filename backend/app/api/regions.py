"""Region routes"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from app.db.database import get_db
from app.schemas.region import RegionCreate, RegionResponse
from app.crud.region import create_region, get_all_regions, get_region_by_id, update_region
from app.core.deps import get_admin_user

router = APIRouter(prefix="/api/v1/regions", tags=["Regions"])

@router.get("", response_model=list[RegionResponse])
def get_regions(db: Session = Depends(get_db)):
    """Get all available regions"""
    regions = get_all_regions(db)
    return regions

@router.post("", response_model=RegionResponse, status_code=status.HTTP_201_CREATED)
def create_new_region(
    region: RegionCreate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_admin_user)
):
    """Create a new region (Admin only)"""
    db_region = create_region(db, region)
    return db_region

@router.get("/{region_id}", response_model=RegionResponse)
def get_region(region_id: UUID, db: Session = Depends(get_db)):
    """Get region by ID"""
    region = get_region_by_id(db, region_id)
    if not region:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Region not found")
    return region
