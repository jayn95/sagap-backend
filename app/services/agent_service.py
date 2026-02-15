from sqlalchemy.orm import Session
from app.db import models
from app.schemas.agent import AgentCreate


def create_agent(db: Session, agent: AgentCreate) -> models.Agent:
    """
    Creates a new agent in the database using validated schema data.
    Returns the newly created Agent object.
    """
    new_agent = models.Agent(**agent.model_dump())

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent


def get_all_agents(db: Session):
    """
    Retrieves all agents from the database.
    """
    return db.query(models.Agent).all()


def get_agent_by_id(db: Session, agent_id: int):
    """
    Retrieves a specific agent using agent_id.
    """
    return db.query(models.Agent).filter(
        models.Agent.agent_id == agent_id
    ).first()


def delete_agent(db: Session, agent_id: int):
    """
    Deletes an agent record if it exists.
    Returns True if successful.
    """
    agent = db.query(models.Agent).filter(
        models.Agent.agent_id == agent_id
    ).first()

    if agent:
        db.delete(agent)
        db.commit()
        return True

    return False
