"""
Pydantic schemas for asset assignment API requests and responses.
Used for data validation and serialization.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AssignmentBase(BaseModel):
    asset_id: int
    agent_id: int
    remarks: Optional[str] = None

class AssignmentCreate(AssignmentBase):
    pass

class AssignmentUpdate(BaseModel):
    agent_id: Optional[int] = None
    remarks: Optional[str] = None

class AssignmentRead(AssignmentBase):
    assignment_id: int
    assigned_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# ALL ASSETS WITH CURRENT OWNERS
class AssetOwnerRead(BaseModel):
    assignment_id: int

    asset_id: int
    asset_tag: str | None = None
    asset_type: str | None = None

    agent_id: int
    agent_name: str | None = None

    assigned_at: datetime

    class Config:
        orm_mode = True