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

class AssignmentRead(AssignmentBase):
    assignment_id: int
    assigned_at: datetime
    returned_at: Optional[datetime] = None

    class Config:
        orm_mode = True
