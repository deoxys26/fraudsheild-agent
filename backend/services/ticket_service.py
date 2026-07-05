from datetime import datetime
from sqlalchemy.orm import Session


from models.db_models import Ticket


def generate_ticket_id(db: Session) -> str:
    count = db.query(Ticket).count()
    return f"SBI-FRD-{count + 1:03d}"


def create_ticket(db: Session, ticket_data: dict) -> Ticket:
    ticket_id = generate_ticket_id(db)

    ticket = Ticket(
        ticket_id=ticket_id,
        status="Open",
        **ticket_data
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return ticket


def get_all_tickets(
    db: Session,
    status: str | None = None,
    severity: str | None = None,
    category: str | None = None
):
    query = db.query(Ticket)

    if status:
        query = query.filter(Ticket.status == status)

    if severity:
        query = query.filter(Ticket.severity == severity)

    if category:
        query = query.filter(Ticket.category == category)

    return query.order_by(Ticket.created_at.desc()).all()


def get_ticket_by_id(db: Session, ticket_id: str):
    return db.query(Ticket).filter(Ticket.ticket_id == ticket_id).first()


def update_ticket_status(db: Session, ticket_id: str, status: str):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return None

    ticket.status = status
    ticket.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket


def delete_ticket(db: Session, ticket_id: str) -> bool:
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return False

    db.delete(ticket)
    db.commit()

    return True


def update_officer_note(db: Session, ticket_id: str, note: str):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return None

    ticket.officer_note = note
    ticket.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket



def update_collected_details(db: Session, ticket_id: str, collected_details: dict):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        return None

    ticket.collected_details = collected_details
    ticket.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(ticket)

    return ticket