from sqlalchemy.orm import Session
from models.db_models import AuditLog


def create_audit_log(
    db: Session,
    ticket_id: str,
    action: str,
    details: str | None = None
) -> AuditLog:
    log = AuditLog(
        ticket_id=ticket_id,
        action=action,
        details=details
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    return log


def get_audit_logs_by_ticket(db: Session, ticket_id: str):
    return (
        db.query(AuditLog)
        .filter(AuditLog.ticket_id == ticket_id)
        .order_by(AuditLog.created_at.desc())
        .all()
    )