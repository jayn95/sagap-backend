"""
Service layer for generating reports.
Handles FATR and Desktop Assignment Form generation.
"""

from sqlalchemy.orm import Session
from app.db.models import AssetAssignment
from typing import List, Dict

def get_all_assignments(db: Session) -> List[AssetAssignment]:
    """
    Retrieves all asset assignments from the database.
    Used as source data for reports.
    """
    return db.query(AssetAssignment).all()


def generate_fatr_report(db: Session) -> List[Dict]:
    """
    Generates FATR report data.
    Returns a list of dictionaries with assignment details.
    """
    assignments = get_all_assignments(db)
    report = []
    for a in assignments:
        report.append({
            "assignment_id": a.assignment_id,
            "asset_tag": a.asset.asset_tag,
            "asset_name": a.asset.asset_name,
            "agent_name": a.agent.full_name,
            "assigned_at": a.assigned_at,
            "returned_at": a.returned_at,
            "remarks": a.remarks
        })
    return report


def generate_desktop_assignment_form(db: Session) -> List[Dict]:
    """
    Generates Desktop Assignment Form data.
    Returns list of assignments grouped by agent.
    """
    assignments = get_all_assignments(db)
    report = []
    for a in assignments:
        report.append({
            "agent_name": a.agent.full_name,
            "employee_no": a.agent.employee_no,
            "asset_tag": a.asset.asset_tag,
            "asset_name": a.asset.asset_name,
            "assigned_at": a.assigned_at
        })
    return report
