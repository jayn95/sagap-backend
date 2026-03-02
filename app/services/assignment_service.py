from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from app.db.models import Asset, Agent, AssetAssignment

def assign_asset(db: Session, asset_id: int, agent_id: int, remarks: str | None = None):
    # Check asset exists
    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()
    if not asset:
        raise ValueError("Asset not found")

    # Check agent exists
    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
    if not agent:
        raise ValueError("Agent not found")

    # Check if asset is already assigned
    active_assignment = db.query(AssetAssignment).filter(
        and_(
            AssetAssignment.asset_id == asset_id,
            AssetAssignment.returned_at == None
        )
    ).first()

    if active_assignment:
        raise ValueError("Asset is already assigned")

    # Create assignment
    assignment = AssetAssignment(
        asset_id=asset_id,
        agent_id=agent_id,
        remarks=remarks
    )

    # Update asset status
    asset.status = "Assigned"

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return assignment


def return_asset(db: Session, assignment_id: int):
    assignment = db.query(AssetAssignment).filter(
        AssetAssignment.assignment_id == assignment_id
    ).first()

    if not assignment:
        raise ValueError("Assignment not found")

    if assignment.returned_at is not None:
        raise ValueError("Asset already returned")

    assignment.returned_at = datetime.utcnow()

    # Update asset status
    assignment.asset.status = "Available"

    db.commit()
    db.refresh(assignment)

    return assignment

# Update Assignment logic (EDIT MARKS OR AGENT)
def update_assignment(
    db: Session,
    assignment_id: int,
    agent_id: int | None = None,
    remarks: str | None = None,
):
    assignment = db.query(AssetAssignment).filter(
        AssetAssignment.assignment_id == assignment_id
    ).first()

    if not assignment:
        raise ValueError("Assignment not found")

    # Optional: change agent
    if agent_id is not None:
        agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()
        if not agent:
            raise ValueError("Agent not found")
        assignment.agent_id = agent_id

    # Optional: update remarks
    if remarks is not None:
        assignment.remarks = remarks

    db.commit()
    db.refresh(assignment)

    return assignment

# Delete Assignment logic
def delete_assignment(db: Session, assignment_id: int):
    """
    Soft delete only allowed if assignment was created by mistake
    and asset was never returned nor used historically.
    """

    assignment = db.query(AssetAssignment).filter(
        AssetAssignment.assignment_id == assignment_id,
        AssetAssignment.is_deleted == False
    ).first()

    if not assignment:
        raise ValueError("Assignment not found")

    # If asset already returned → history exists → DO NOT DELETE
    if assignment.returned_at is not None:
        raise ValueError("Cannot delete historical assignment record")

    # Allow deletion only before return (input mistake scenario)
    assignment.is_deleted = True

    # Restore asset status
    assignment.asset.status = "Available"

    db.commit()

    return True

# Get all assignments via service
# Hide Deleted Records Automatically
def get_all_assignments(db: Session):
    return db.query(AssetAssignment).filter(
        AssetAssignment.is_deleted == False
    ).all()

# ASSET HISTORY
def get_asset_history(db: Session, asset_id: int):
    """
    Returns the full assignment history of a specific asset,
    including past and current owners.
    """

    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()

    if not asset:
        raise ValueError("Asset not found")

    history = db.query(AssetAssignment).filter(
        AssetAssignment.asset_id == asset_id,
        AssetAssignment.is_deleted == False
    ).order_by(AssetAssignment.assigned_at.asc()).all()

    return history


# ASSETS CURRENT OWNER
def get_current_owner(db: Session, asset_id: int):
    """
    Returns the current owner of an asset (active assignment).
    """

    asset = db.query(Asset).filter(Asset.asset_id == asset_id).first()

    if not asset:
        raise ValueError("Asset not found")

    assignment = db.query(AssetAssignment).filter(
        AssetAssignment.asset_id == asset_id,
        AssetAssignment.returned_at == None,
        AssetAssignment.is_deleted == False
    ).first()

    if not assignment:
        raise ValueError("Asset is currently not assigned")

    return assignment

# AGENT CURENT ASSETS
def get_agent_current_assets(db: Session, agent_id: int):
    """
    Returns all assets currently assigned to a specific agent.
    """

    agent = db.query(Agent).filter(Agent.agent_id == agent_id).first()

    if not agent:
        raise ValueError("Agent not found")

    assignments = db.query(AssetAssignment).filter(
        AssetAssignment.agent_id == agent_id,
        AssetAssignment.returned_at == None,
        AssetAssignment.is_deleted == False
    ).all()

    return assignments

# OVERVIEW OF ALL ASSETS WITH CURRENT OWNERS: ONE ASSET - ONE OWNER, ONE AGENT - MANY ASSETS
def get_all_current_asset_owners(db: Session):
    """
    Returns all assets that currently have an owner.
    Each asset will appear only once because only one active assignment is allowed.
    """

    assignments = db.query(AssetAssignment).filter(
        AssetAssignment.returned_at == None,
        AssetAssignment.is_deleted == False
    ).all()

    results = []

    for a in assignments:
        results.append({
            "assignment_id": a.assignment_id,

            "asset_id": a.asset.asset_id,
            "asset_tag": a.asset.asset_tag,
            "asset_type": a.asset.asset_type,

            "agent_id": a.agent.agent_id,
            "agent_name": a.agent.full_name,

            "assigned_at": a.assigned_at
        })

    return results