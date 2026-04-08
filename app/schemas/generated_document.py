"""
Pydantic schemas for report generation.
Used for serialization of FATR and Desktop Assignment Form data.
"""

from pydantic import BaseModel
from typing import Any
from datetime import datetime


class GeneratedDocumentResponse(BaseModel):
    id: int
    agent_id: int
    set_assignment_id: int | None
    document_type: str
    document_data: Any
    created_at: datetime

    class Config:
        orm_mode = True