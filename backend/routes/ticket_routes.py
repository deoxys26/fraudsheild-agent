from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from services.audit_service import get_audit_logs_by_ticket
from services.notification_service import get_alerts_by_ticket
from typing import List, Optional
from models.schemas import TicketStatusUpdate, TicketResponse, OfficerNoteUpdate
from services.ticket_service import (
    get_all_tickets,
    get_ticket_by_id,
    update_ticket_status,
    update_officer_note,
    delete_ticket
)
from models.schemas import TicketStatusUpdate, TicketResponse, OfficerNoteUpdate, TicketDetailsUpdate

from database import get_db
from models.schemas import TicketStatusUpdate, TicketResponse
from services.ticket_service import (
    get_all_tickets,
    get_ticket_by_id,
    update_ticket_status,
    update_officer_note,
    update_collected_details,
    delete_ticket
)
from services.audit_service import create_audit_log

router = APIRouter(
    prefix="/api/tickets",
    tags=["Tickets"]
)


@router.get("/", response_model=List[TicketResponse])
def get_tickets(
    status: Optional[str] = None,
    severity: Optional[str] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return get_all_tickets(
        db=db,
        status=status,
        severity=severity,
        category=category
    )

@router.get("/{ticket_id}", response_model=TicketResponse)
def get_ticket(ticket_id: str, db: Session = Depends(get_db)):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket


@router.patch("/{ticket_id}/status", response_model=TicketResponse)
def change_ticket_status(
    ticket_id: str,
    request: TicketStatusUpdate,
    db: Session = Depends(get_db)
):
    updated_ticket = update_ticket_status(db, ticket_id, request.status.value)

    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    create_audit_log(
        db=db,
        ticket_id=ticket_id,
        action="Status Manually Updated",
        details=f"Officer changed ticket status to {request.status.value}."
    )

    return updated_ticket


@router.delete("/{ticket_id}")
def remove_ticket(ticket_id: str, db: Session = Depends(get_db)):
    deleted = delete_ticket(db, ticket_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {
        "message": f"Ticket {ticket_id} deleted successfully"
    }
@router.get("/{ticket_id}/audit-logs")
def get_ticket_audit_logs(ticket_id: str, db: Session = Depends(get_db)):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return get_audit_logs_by_ticket(db, ticket_id)


@router.get("/{ticket_id}/alerts")
def get_ticket_alerts(ticket_id: str, db: Session = Depends(get_db)):
    ticket = get_ticket_by_id(db, ticket_id)

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return get_alerts_by_ticket(db, ticket_id)

@router.patch("/{ticket_id}/note", response_model=TicketResponse)
def add_officer_note(
    ticket_id: str,
    request: OfficerNoteUpdate,
    db: Session = Depends(get_db)
):
    updated_ticket = update_officer_note(db, ticket_id, request.note)

    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    create_audit_log(
        db=db,
        ticket_id=ticket_id,
        action="Officer Note Updated",
        details="Officer added or updated the case note."
    )

    return updated_ticket


@router.patch("/{ticket_id}/details", response_model=TicketResponse)
def update_missing_details(
    ticket_id: str,
    request: TicketDetailsUpdate,
    db: Session = Depends(get_db)
):
    updated_ticket = update_collected_details(
        db=db,
        ticket_id=ticket_id,
        collected_details=request.collected_details
    )

    if not updated_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    create_audit_log(
        db=db,
        ticket_id=ticket_id,
        action="Missing Details Updated",
        details="Officer collected and saved required case details."
    )

    return updated_ticket