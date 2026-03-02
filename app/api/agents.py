from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.agent import AgentCreate, AgentRead
from app.services import agent_service, assignment_service
from app.schemas.agent import AgentUpdate
from app.schemas.assignment import AssignmentRead

router = APIRouter(prefix="/agents", tags=["Agents"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- CREATE ----------
@router.post("/", response_model=AgentRead)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """
    Creates a new agent.
    Delegates creation to agent_service.
    """
    return agent_service.create_agent(db, agent)

# ---------- SPECIAL LIST ----------
@router.get("/", response_model=List[AgentRead])
def get_all_agents(db: Session = Depends(get_db)):
    """
    Retrieves all agents.
    Delegates retrieval to agent_service.
    """
    return agent_service.get_all_agents(db)

# AGENTS CURRENT ASSETS ENDPOINT
@router.get("/{agent_id}/assets", response_model=List[AssignmentRead])
def get_agent_current_assets(agent_id: int, db: Session = Depends(get_db)):
    """
    Retrieves all assets currently assigned to an agent.
    """
    try:
        return assignment_service.get_agent_current_assets(db, agent_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
# ---------- UPDATE ----------
# Update Agent Endpoint
@router.put("/{agent_id}", response_model=AgentRead)
def update_agent(agent_id: int, payload: AgentUpdate, db: Session = Depends(get_db)):
    """
    Updates agent information.
    """
    try:
        return agent_service.update_agent(db, agent_id, payload)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# ---------- GET SINGLE ----------
@router.get("/{agent_id}", response_model=AgentRead)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single agent by ID.
    Returns 404 if not found.
    """
    agent = agent_service.get_agent_by_id(db, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

# ---------- DELETE ----------
@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Deletes an agent by ID.
    Prevents deletion if agent has assignment history.
    """
    try:
        deleted = agent_service.delete_agent(db, agent_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Agent not found")

        return {"message": "Agent deleted successfully"}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))