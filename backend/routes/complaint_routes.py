from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.schemas import ComplaintRequest, FinalComplaintResponse
from services.agent_service import analyze_complaint_with_ai
from services.risk_service import calculate_risk_score
from services.ticket_service import create_ticket
from services.agent_decision_service import execute_agent_actions
from services.audit_service import create_audit_log

complaint_router = APIRouter(
    prefix="/api/complaints",
    tags=["Complaints"]
)


@complaint_router.post("/analyze", response_model=FinalComplaintResponse)
def analyze_complaint(
    request: ComplaintRequest,
    db: Session = Depends(get_db)
):
    try:
        ai_result = analyze_complaint_with_ai(request.complaint)

        risk_result = calculate_risk_score(
            category=ai_result.category,
            amount=ai_result.amount or 0,
            complaint=request.complaint
        )

        ticket = create_ticket(db, {
            "customer_name": request.customer_name,
            "account_last4": request.account_last4,
            "phone": request.phone,
            "original_complaint": request.complaint,
            "category": ai_result.category,
            "amount": ai_result.amount,
            "severity": risk_result["severity"],
            "risk_score": risk_result["risk_score"],
            "priority_reason": ai_result.priority_reason,
            "missing_details": ai_result.missing_details,
            "recommended_action": ai_result.recommended_action,
            "officer_summary": ai_result.officer_summary
        })

        create_audit_log(
            db=db,
            ticket_id=ticket.ticket_id,
            action="Complaint Classified",
            details=f"Complaint classified as {ticket.category} with detected amount ₹{ticket.amount}."
        )

        create_audit_log(
            db=db,
            ticket_id=ticket.ticket_id,
            action="Policy Applied",
            details=f"Policy-grounded missing details and recommended action generated for {ticket.category}."
        )

        create_audit_log(
            db=db,
            ticket_id=ticket.ticket_id,
            action="Risk Score Calculated",
            details=f"Risk score calculated as {ticket.risk_score}. Severity set to {ticket.severity}."
        )

        create_audit_log(
            db=db,
            ticket_id=ticket.ticket_id,
            action="Ticket Created",
            details=f"Ticket {ticket.ticket_id} created in PostgreSQL."
        )

        execute_agent_actions(db, ticket)
        db.refresh(ticket)

        return {
            "ticket_id": ticket.ticket_id,
            "customer_name": ticket.customer_name,
            "account_last4": ticket.account_last4,
            "phone": ticket.phone,
            "original_complaint": ticket.original_complaint,
            "category": ticket.category,
            "amount": ticket.amount,
            "severity": ticket.severity,
            "risk_score": ticket.risk_score,
            "priority_reason": ticket.priority_reason,
            "missing_details": ticket.missing_details,
            "recommended_action": ticket.recommended_action,
            "officer_summary": ticket.officer_summary,
            "status": ticket.status,
            "officer_note": ticket.officer_note,
            "created_at": ticket.created_at,
            "updated_at": ticket.updated_at
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))