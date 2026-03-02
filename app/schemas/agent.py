"""
Pydantic schemas for agent-related API requests and responses.
Used for validating incoming data and formatting outgoing responses.
These schemas mirror the Agent database model structure.
"""

from pydantic import BaseModel
from datetime import datetime


class AgentBase(BaseModel):
    """
    Base schema containing common agent fields.
    Used as a foundation for creating and reading agent records.
    """

    employee_no: str
    full_name: str

    designation: str | None = None
    department: str | None = None

    contact_number: str | None = None
    email: str | None = None
    current_address: str | None = None

    status: str | None = "Active"


class AgentCreate(AgentBase):
    """
    Schema used when creating a new agent.
    Inherits all fields from AgentBase.
    """
    pass


class AgentRead(AgentBase):
    """
    Schema used when returning agent data from the database.
    Includes database-generated fields.
    """

    agent_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# Optional Schema for updating agent information
class AgentUpdate(BaseModel):
    employee_no: str | None = None
    full_name: str | None = None
    designation: str | None = None
    department: str | None = None
    contact_number: str | None = None
    email: str | None = None
    current_address: str | None = None
    status: str | None = None