from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.assignment import AssignmentCreate, AssignmentRead
from app.services import assignment_service

router = APIRouter(prefix="/assignments", tags=["Assignments"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# API Endpoints
# -----------------------------

@router.post("/", response_model=AssignmentRead)
def assign_asset(assignment: AssignmentCreate, db: Session = Depends(get_db)):
    """
    Assigns an asset to an agent.
    Delegates logic to assignment_service.
    """
    try:
        return assignment_service.assign_asset(
            db,
            asset_id=assignment.asset_id,
            agent_id=assignment.agent_id,
            remarks=assignment.remarks
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/return/{assignment_id}", response_model=AssignmentRead)
def return_asset(assignment_id: int, db: Session = Depends(get_db)):
    """
    Marks an assigned asset as returned.
    Delegates logic to assignment_service.
    """
    try:
        return assignment_service.return_asset(db, assignment_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=List[AssignmentRead])
def get_all_assignments(db: Session = Depends(get_db)):
    """
    Retrieves all asset assignments.
    """
    return db.query(assignment_service.AssetAssignment).all()  # Optional: could move to service
