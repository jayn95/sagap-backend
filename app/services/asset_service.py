from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.db import models
from app.schemas.asset import AssetCreate, AssetUpdate


def create_asset(db: Session, asset: AssetCreate) -> models.Asset:
    """
    Creates a new asset in the database using validated schema data.
    Returns the newly created Asset object.
    """
    new_asset = models.Asset(**asset.model_dump())

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    return new_asset


def get_all_assets(db: Session):
    """
    Retrieves all assets from the database.
    """
    # filter out deleted assets
    return db.query(models.Asset).filter(models.Asset.is_deleted == False).all()


def get_asset_by_id(db: Session, asset_id: int):
    """
    Retrieves a specific asset using asset_id.
    """
    return db.query(models.Asset).filter(
        models.Asset.asset_id == asset_id,
        models.Asset.is_deleted == False  # Exclude deleted assets
    ).first()


def delete_asset(db: Session, asset_id: int):
    """
    Deletes an asset record if it exists.

    Business Rule:
    - Prevent deletion if the asset has assignment history.
    - This preserves ownership records and historical tracking.

    Returns True if deleted successfully.
    Raises ValueError if deletion is not allowed.
    """

    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == asset_id
    ).first()

    if not asset:
        return False

    # 🔒 Prevent deletion if asset has assignments
    if asset.assignments:
        raise ValueError("Cannot delete asset with assignment history")
    
    # soft delete: mark as deleted instead of removing from database
    asset.is_deleted = True
    db.commit()

    return True

#Get All Available Assets
# Changed Asset into models.Asset to avoid circular import
def get_available_assets(db: Session):
    return db.query(models.Asset).filter(
        models.Asset.status == "Available",
        models.Asset.is_deleted == False  # Exclude deleted assets
    ).all()


# Update Asset Fields
def update_asset(db: Session, asset_id: int, data: AssetUpdate):
    """
    Updates asset information.
    """

    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == asset_id
    ).first()

    if not asset:
        raise ValueError("Asset not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(asset, field, value)

    db.commit()
    db.refresh(asset)

    return asset

# Asset Search and Feature
def search_assets(
    db: Session,
    asset_type: str | None = None,
    status: str | None = None,
    brand: str | None = None,
    condition: str | None = None,
    assigned: bool | None = None,
    search: str | None = None
):
    """
    Searches and filters assets dynamically based on provided parameters.
    """

    query = db.query(models.Asset).filter(
        models.Asset.is_deleted == False
    )

    # Filters
    if asset_type:
        query = query.filter(models.Asset.asset_type.ilike(f"%{asset_type}%"))

    if status:
        query = query.filter(models.Asset.status.ilike(f"%{status}%"))

    if brand:
        query = query.filter(models.Asset.brand.ilike(f"%{brand}%"))

    if condition:
        query = query.filter(models.Asset.condition.ilike(f"%{condition}%"))

    # Assigned filter
    if assigned is not None:
        if assigned:
            query = query.filter(models.Asset.status == "Assigned")
        else:
            query = query.filter(models.Asset.status == "Available")

    # Text search
    if search:
        query = query.filter(
            or_(
                models.Asset.asset_tag.ilike(f"%{search}%"),
                models.Asset.brand.ilike(f"%{search}%"),
                models.Asset.model.ilike(f"%{search}%"),
                models.Asset.serial_number.ilike(f"%{search}%"),
            )
        )

    return query.all()