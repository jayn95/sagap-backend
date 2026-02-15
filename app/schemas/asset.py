"""
Pydantic schemas for asset-related API requests and responses.
Used for validating incoming asset data and formatting database responses.
Supports Desktop, Monitor, and Peripheral asset types.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AssetBase(BaseModel):
    """
    Base schema containing common asset fields.
    Used for creating and reading asset records.
    """

    asset_type: str
    # Examples: Desktop, Monitor, Keyboard, Mouse, IP Phone, etc.

    asset_tag: str

    brand: Optional[str] = None
    model: Optional[str] = None

    serial_number: Optional[str] = None
    serial_number_2: Optional[str] = None  # Used for Monitor (optional)

    memory: Optional[str] = None  # Used for Desktop (optional)

    condition: Optional[str] = "Good"

    status: Optional[str] = "Available"


class AssetCreate(AssetBase):
    """
    Schema used when creating a new asset.
    Inherits all fields from AssetBase.
    """
    pass


class AssetRead(AssetBase):
    """
    Schema used when returning asset data from the database.
    Includes database-generated fields.
    """

    asset_id: int
    created_at: datetime

    class Config:
        orm_mode = True
