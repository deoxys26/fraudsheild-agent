import os
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from services.audit_service import create_audit_log
from services.notification_service import (
    create_alert,
    send_email_alert,
    update_alert_status
)
from services.ticket_service import update_ticket_status

load_dotenv()

OFFICER_EMAIL = os.getenv("ALERT_RECIPIENT_EMAIL", "fraud-officer@sbi-demo.com")


def execute_agent_actions(db: Session, ticket):
    severity = ticket.severity
    ticket_id = ticket.ticket_id

    if severity in ["Critical", "High"]:
        update_ticket_status(db, ticket_id, "Escalated")

        create_audit_log(
            db=db,
            ticket_id=ticket_id,
            action="Status Auto-Updated",
            details=f"Ticket status changed to Escalated because severity is {severity}."
        )

        alert_message = (
            f"High-risk fraud complaint detected.\n\n"
            f"Ticket ID: {ticket.ticket_id}\n"
            f"Category: {ticket.category}\n"
            f"Amount: ₹{ticket.amount}\n"
            f"Severity: {ticket.severity}\n"
            f"Risk Score: {ticket.risk_score}\n\n"
            f"Priority Reason:\n{ticket.priority_reason}\n\n"
            f"Officer Summary:\n{ticket.officer_summary}\n\n"
            f"Recommended Action:\n{ticket.recommended_action}"
        )

        alert = create_alert(
            db=db,
            ticket_id=ticket_id,
            alert_type="Email",
            recipient=OFFICER_EMAIL,
            message=alert_message,
            status="Pending"
        )

        create_audit_log(
            db=db,
            ticket_id=ticket_id,
            action="Alert Created",
            details=f"Email alert created for {OFFICER_EMAIL}."
        )

        email_sent = send_email_alert(
            subject=f"[FraudShield] {severity} Fraud Alert - {ticket.ticket_id}",
            body=alert_message,
            recipient=OFFICER_EMAIL
        )

        if email_sent:
            update_alert_status(db, alert.id, "Sent")
            create_audit_log(
                db=db,
                ticket_id=ticket_id,
                action="Email Alert Sent",
                details=f"Email alert successfully sent to {OFFICER_EMAIL}."
            )
        else:
            update_alert_status(db, alert.id, "Failed")
            create_audit_log(
                db=db,
                ticket_id=ticket_id,
                action="Email Alert Failed",
                details=f"Email alert failed for {OFFICER_EMAIL}. Check SMTP credentials or app password."
            )

    elif severity == "Medium":
        update_ticket_status(db, ticket_id, "In Review")

        create_audit_log(
            db=db,
            ticket_id=ticket_id,
            action="Status Auto-Updated",
            details="Ticket status changed to In Review for officer verification."
        )

    else:
        create_audit_log(
            db=db,
            ticket_id=ticket_id,
            action="No Alert Needed",
            details="Low-risk ticket saved without escalation or email alert."
        )