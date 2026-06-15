"""Region CRUD operations"""
from sqlalchemy.orm import Session
from uuid import UUID
from app.models.region import Region
from app.schemas.region import RegionCreate
from app.core.exceptions import NotFound

def create_region(db: Session, region: RegionCreate) -> Region:
    """Create a new region"""
    db_region = Region(
        name=region.name,
        description=region.description,
        timezone=region.timezone
    )
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

def get_all_regions(db: Session):
    """Get all active regions"""
    return db.query(Region).filter(Region.is_active == True).all()

def get_region_by_id(db: Session, region_id: UUID) -> Region:
    """Get region by ID"""
    return db.query(Region).filter(Region.region_id == region_id).first()

def update_region(db: Session, region_id: UUID, region_update: RegionCreate) -> Region:
    """Update a region"""
    db_region = get_region_by_id(db, region_id)
    if not db_region:
        raise NotFound("Region")
    
    db_region.name = region_update.name
    db_region.description = region_update.description
    db_region.timezone = region_update.timezone
    db.commit()
    db.refresh(db_region)
    return db_region
