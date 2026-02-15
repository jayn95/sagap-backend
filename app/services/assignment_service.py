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
