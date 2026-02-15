from sqlalchemy.orm import Session
from app.db import models
from app.schemas.asset import AssetCreate


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
    return db.query(models.Asset).all()


def get_asset_by_id(db: Session, asset_id: int):
    """
    Retrieves a specific asset using asset_id.
    """
    return db.query(models.Asset).filter(
        models.Asset.asset_id == asset_id
    ).first()


def delete_asset(db: Session, asset_id: int):
    """
    Deletes an asset record if it exists.
    Returns True if successful.
    """
    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == asset_id
    ).first()

    if asset:
        db.delete(asset)
        db.commit()
        return True

    return False
