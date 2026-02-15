from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.agent import AgentCreate, AgentRead
from app.services import agent_service

router = APIRouter(prefix="/agents", tags=["Agents"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=AgentRead)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """
    Creates a new agent.
    Delegates creation to agent_service.
    """
    return agent_service.create_agent(db, agent)


@router.get("/", response_model=List[AgentRead])
def get_all_agents(db: Session = Depends(get_db)):
    """
    Retrieves all agents.
    Delegates retrieval to agent_service.
    """
    return agent_service.get_all_agents(db)


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


@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Deletes an agent by ID.
    Returns 404 if agent not found.
    """
    deleted = agent_service.delete_agent(db, agent_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"message": "Agent deleted successfully"}
