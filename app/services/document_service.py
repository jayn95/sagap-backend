"""
Service layer for generating reports.
Handles FATR and Desktop Assignment Form generation.
"""

from sqlalchemy.orm import Session
from app.db import models


def create_generated_document(
    db: Session,
    agent_id: int,
    set_assignment_id: int | None,
    document_type: str,
    document_payload: dict
) -> models.GeneratedDocument:
    """
    Creates and stores a generated document record in the database.
    Stores structured JSON data for later PDF generation.
    """

    document = models.GeneratedDocument(
        agent_id=agent_id,
        set_assignment_id=set_assignment_id,  # Can be None
        document_type=document_type,
        document_data=document_payload
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

def build_desktop_json(agent, assignments) -> dict:
    """
    Builds structured JSON data for Desktop Assignment Form.
    Includes all active assigned assets of the agent.
    """

    assets_list = []

    for assignment in assignments:
        asset = assignment.asset

        # Defensive check (avoid crashes if relationship missing)
        if not asset:
            continue

        assets_list.append({
            "asset_id": asset.asset_id,
            "asset_type": asset.asset_type,
            "brand": asset.brand,
            "model": asset.model,
            "serial_number": asset.serial_number,
            "asset_tag": asset.asset_tag,
            "status": asset.status
        })

    document_payload = {
        "document_type": "DESKTOP_ASSIGNMENT_FORM",
        "agent": {
            "agent_id": agent.agent_id,
            "full_name": agent.full_name,
            "department": agent.department,
            "designation": agent.designation,
            "email": agent.email
        },
        "assets": assets_list,
        "total_assets": len(assets_list)
    }

    return document_payload

def build_fatr_json(agent, assignments) -> dict:
    """
    Builds structured JSON data for Fixed Asset Transfer Report (FATR).
    Includes only assets marked as fixed assets.
    """

    fixed_assets_list = []

    for assignment in assignments:
        asset = assignment.asset

        # Defensive check
        if not asset:
            continue

        # Include only fixed assets
        if not asset.is_fixed_asset:
            continue

        fixed_assets_list.append({
            "asset_id": asset.asset_id,
            "asset_type": asset.asset_type,
            "brand": asset.brand,
            "model": asset.model,
            "serial_number": asset.serial_number,
            "asset_tag": asset.asset_tag,
            "condition": asset.condition,
            "status": asset.status
        })

    document_payload = {
        "document_type": "FATR",
        "transfer_details": {
            "new_owner": {
                "agent_id": agent.agent_id,
                "full_name": agent.full_name,
                "department": agent.department,
                "designation": agent.designation
            }
        },
        "fixed_assets": fixed_assets_list,
        "total_fixed_assets": len(fixed_assets_list)
    }

    return document_payload

# Service Functions to retrieve generated documents
def get_documents_by_agent(db: Session, agent_id: int):
    return db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.agent_id == agent_id
    ).order_by(models.GeneratedDocument.created_at.desc()).all()


def get_document_by_id(db: Session, document_id: int):
    return db.query(models.GeneratedDocument).filter(
        models.GeneratedDocument.id == document_id
    ).first()