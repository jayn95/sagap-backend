from sqlalchemy.orm import Session
from app.db import models
from app.schemas.agent import AgentCreate, AgentUpdate
# from app.services.audit_service import log_action

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
    #Added changes to filter out deleted agents
    return db.query(models.Agent).filter(models.Agent.is_deleted == False).all()


def get_agent_by_id(db: Session, agent_id: int):
    """
    Retrieves a specific agent using agent_id.
    """
    return db.query(models.Agent).filter(
        models.Agent.agent_id == agent_id,
        models.Agent.is_deleted == False  # Exclude deleted agents
    ).first()


def delete_agent(db: Session, agent_id: int):
    """
    Deletes an agent record if it exists.

    Business Rule:
    - Prevent deletion if the agent has assignment history.
    - This preserves asset ownership records and data integrity.

    Returns True if deleted successfully.
    Raises ValueError if deletion is not allowed.
    """

    agent = db.query(models.Agent).filter(
        models.Agent.agent_id == agent_id
    ).first()

    if not agent:
        return False

    # 🔒 Prevent deletion if agent has assignments
    if agent.assignments:
        raise ValueError("Cannot delete agent with assignment history")
    
    # soft delete: mark as deleted instead of removing from database
    agent.is_deleted = True
    db.commit()

    return True

# Update Agent Fields
def update_agent(db: Session, agent_id: int, data: AgentUpdate):
    """
    Updates an existing agent.
    """

    agent = db.query(models.Agent).filter(
        models.Agent.agent_id == agent_id
    ).first()

    if not agent:
        raise ValueError("Agent not found")

    update_data = data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(agent, field, value)

    db.commit()
    db.refresh(agent)

    return agent

# Audit logs