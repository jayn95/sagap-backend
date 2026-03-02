from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Agent(Base):
    """
    Represents an employee (agent) in the inventory system.

    Stores employee personal and organizational details.
    Agents can be assigned assets, and assignment history
    is tracked through the AssetAssignment table.
    """

    __tablename__ = "agents"

    agent_id = Column(Integer, primary_key=True, index=True)

    employee_no = Column(String(50), unique=True, index=True, nullable=False)

    full_name = Column(String(150), nullable=False)

    designation = Column(String(100))  # replaces "position"

    department = Column(String(100))

    contact_number = Column(String(50))

    email = Column(String(150))

    current_address = Column(Text)

    status = Column(String(50), default="Active")

    # Soft delete flag for agents (not currently used in API, but available for future use)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())

    # Relationship: One agent can have many asset assignments
    assignments = relationship("AssetAssignment", back_populates="agent")


class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)

    asset_type = Column(String(50), nullable=False)

    asset_tag = Column(String(100), unique=True, index=True)

    brand = Column(String(100))
    model = Column(String(100))

    serial_number = Column(String(100))
    serial_number_2 = Column(String(100))

    memory = Column(String(50))

    condition = Column(String(50), default="Good")

    status = Column(String(50), default="Available")

    # Soft delete flag for assets (not currently used in API, but available for future use)
    is_deleted = Column(Boolean, default=False)

    created_at = Column(DateTime, server_default=func.now())

    assignments = relationship("AssetAssignment", back_populates="asset")


class AssetAssignment(Base):
    __tablename__ = "asset_assignments"

    assignment_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.agent_id"), nullable=False)

    assigned_at = Column(DateTime, server_default=func.now())
    returned_at = Column(DateTime, nullable=True)
    remarks = Column(Text)

    is_deleted = Column(Boolean, default=False)  # NEW FIELD

    # 🔗 relationships
    asset = relationship("Asset", back_populates="assignments")
    agent = relationship("Agent", back_populates="assignments")

# Audit Logs
class AuditLog(Base):
    """
    Stores system activity logs for tracking actions performed
    on agents, assets, and assignments.
    """

    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, index=True)

    action = Column(String(50))          # CREATE, UPDATE, DELETE, ASSIGN, RETURN
    entity = Column(String(50))          # Agent, Asset, Assignment
    entity_id = Column(Integer)          # ID of affected record

    performed_by = Column(String(150))   # user/admin (future auth)

    details = Column(Text)               # optional description

    created_at = Column(DateTime, server_default=func.now())