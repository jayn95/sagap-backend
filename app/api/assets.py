from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.asset import AssetCreate, AssetRead
from app.services import asset_service

router = APIRouter(prefix="/assets", tags=["Assets"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# API Endpoints
# -----------------------------

@router.post("/", response_model=AssetRead)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """
    Creates a new asset record.
    Delegates creation to asset_service.
    """
    return asset_service.create_asset(db, asset)


@router.get("/", response_model=List[AssetRead])
def get_all_assets(db: Session = Depends(get_db)):
    """
    Retrieves all assets from the database.
    Delegates retrieval to asset_service.
    """
    return asset_service.get_all_assets(db)


@router.get("/{asset_id}", response_model=AssetRead)
def get_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single asset by ID.
    Returns 404 if not found.
    """
    asset = asset_service.get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    Deletes an asset by ID.
    Returns 404 if asset not found.
    """
    deleted = asset_service.delete_asset(db, asset_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Asset not found")
    return {"message": "Asset deleted successfully"}
