from sqlalchemy.orm import Session
from app.db.models import AuditLog


def log_action(
    db: Session,
    action: str,
    entity: str,
    entity_id: int | None = None,
    performed_by: int | None = None,
    details: str | None = None
):
    """
    Creates an audit log entry.
    """

    log = AuditLog(
        action=action,
        entity=entity,
        entity_id=entity_id,
        performed_by=performed_by,
        details=details
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log