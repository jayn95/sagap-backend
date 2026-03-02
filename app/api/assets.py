from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.asset import AssetCreate, AssetRead
from app.services import asset_service, assignment_service
from app.schemas.assignment import AssignmentRead, AssetOwnerRead
from app.schemas.asset import AssetUpdate

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

# ---------- CREATE ----------
@router.post("/", response_model=AssetRead)
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    """
    Creates a new asset record.
    Delegates creation to asset_service.
    """
    return asset_service.create_asset(db, asset)

# ---------- SPECIAL LIST ----------
# @router.get("/", response_model=List[AssetRead])
# def get_all_assets(db: Session = Depends(get_db)):
#     """
#     Retrieves all assets from the database.
#     Delegates retrieval to asset_service.
#     """
#     return asset_service.get_all_assets(db)

# Asset Search and Filter Endpoint
@router.get("/", response_model=List[AssetRead])
def search_assets(
    asset_type: str | None = None,
    status: str | None = None,
    brand: str | None = None,
    condition: str | None = None,
    assigned: bool | None = None,
    search: str | None = None,
    db: Session = Depends(get_db)
):
    """
    Search and filter assets.
    All parameters are optional.
    """
    return asset_service.search_assets(
        db=db,
        asset_type=asset_type,
        status=status,
        brand=brand,
        condition=condition,
        assigned=assigned,
        search=search
    )

# API END[POINT] TO GET ALL ASSETS WITH CURRENT OWNERS
@router.get("/current-owners", response_model=List[AssetOwnerRead])
def get_all_current_asset_owners(db: Session = Depends(get_db)):
    """
    Retrieves all assets that currently have an owner.
    """
    return assignment_service.get_all_current_asset_owners(db)

# Available Assets Endpoint
@router.get("/available", response_model=List[AssetRead])
def get_available_assets(db: Session = Depends(get_db)):
    return asset_service.get_available_assets(db)

# ---------- SINGLE RESOURCE ACTIONS ----------
#API endpoint to get asset history
@router.get("/{asset_id}/history", response_model=List[AssignmentRead])
def get_asset_history(asset_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the full ownership history of an asset.
    """
    try:
        return assignment_service.get_asset_history(db, asset_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
#API endpoint to get current owner of an asset
@router.get("/{asset_id}/current-owner", response_model=AssignmentRead)
def get_current_owner(asset_id: int, db: Session = Depends(get_db)):
    """
    Retrieves the current owner of an asset.
    """
    try:
        return assignment_service.get_current_owner(db, asset_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ---------- UPDATE ----------
# Update Asset Endpoint
@router.put("/{asset_id}", response_model=AssetRead)
def update_asset(asset_id: int, payload: AssetUpdate, db: Session = Depends(get_db)):
    """
    Updates asset information.
    """
    try:
        return asset_service.update_asset(db, asset_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))   

# ---------- GET SINGLE ----------
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

# ---------- DELETE ----------
@router.delete("/{asset_id}")
def delete_asset(asset_id: int, db: Session = Depends(get_db)):
    """
    Deletes an asset by ID.
    Prevents deletion if asset has assignment history.
    """
    try:
        deleted = asset_service.delete_asset(db, asset_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Asset not found")

        return {"message": "Asset deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))