"""
Pydantic schemas for report generation.
Used for serialization of FATR and Desktop Assignment Form data.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FATRItem(BaseModel):
    assignment_id: int
    asset_tag: str
    asset_name: str
    agent_name: str
    assigned_at: datetime
    returned_at: Optional[datetime] = None
    remarks: Optional[str] = None

    class Config:
        orm_mode = True

class DesktopAssignmentItem(BaseModel):
    agent_name: str
    employee_no: str
    asset_tag: str
    asset_name: str
    assigned_at: datetime

    class Config:
        orm_mode = True
