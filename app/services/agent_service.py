from sqlalchemy.orm import Session
from app.db import models
from app.schemas.agent import AgentCreate, AgentUpdate
from app.services.audit_service import log_action

def create_agent(db: Session, agent: AgentCreate) -> models.Agent:
    """
    Creates a new agent in the database using validated schema data.
    Returns the newly created Agent object.
    """
    new_agent = models.Agent(**agent.model_dump())

    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    # Audit log after create commit
    log_action(
        db,
        action="CREATE",
        entity="Agent",
        entity_id=new_agent.agent_id,
        details=f"Agent {new_agent.full_name} created"
    )

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
    Soft deletes an agent record if it exists.

    Business Rules:
    - Prevent deletion if the agent has assignment history.
    - Preserve asset ownership records and data integrity.
    - Use soft delete (is_deleted=True) instead of removing the record.

    Returns True if deleted successfully.
    Raises ValueError if deletion is not allowed.
    """

    agent = db.query(models.Agent).filter(
        models.Agent.agent_id == agent_id,
        models.Agent.is_deleted == False
    ).first()

    if not agent:
        return False

    # 🔒 Prevent deletion if agent has assignment history
    if agent.assignments:
        raise ValueError("Cannot delete agent with assignment history")

    # Soft delete
    agent.is_deleted = True
    db.commit()

    # Audit log after soft delete commit
    log_action(
        db,
        action="DELETE",
        entity="Agent",
        entity_id=agent.agent_id,
        details=f"Agent {agent.full_name} soft deleted"
    )

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

    # Audit log after update commit
    log_action(
        db,
        action="UPDATE",
        entity="Agent",
        entity_id=agent.agent_id,
        details="Agent information updated"
    )

    return agent

# Audit logs