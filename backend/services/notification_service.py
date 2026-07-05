import os
import smtplib
from email.message import EmailMessage
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from models.db_models import Alert

load_dotenv()

ALERT_EMAIL_USER = os.getenv("ALERT_EMAIL_USER")
ALERT_EMAIL_PASSWORD = os.getenv("ALERT_EMAIL_PASSWORD")
ALERT_RECIPIENT_EMAIL = os.getenv("ALERT_RECIPIENT_EMAIL")


def create_alert(
    db: Session,
    ticket_id: str,
    alert_type: str,
    recipient: str,
    message: str,
    status: str = "Pending"
) -> Alert:
    alert = Alert(
        ticket_id=ticket_id,
        alert_type=alert_type,
        recipient=recipient,
        message=message,
        status=status
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def send_email_alert(subject: str, body: str, recipient: str) -> bool:
    if not ALERT_EMAIL_USER or not ALERT_EMAIL_PASSWORD:
        return False

    email = EmailMessage()
    email["From"] = ALERT_EMAIL_USER
    email["To"] = recipient
    email["Subject"] = subject
    email.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(ALERT_EMAIL_USER, ALERT_EMAIL_PASSWORD)
            smtp.send_message(email)

        return True

    except Exception as e:
        print(f"Email sending failed: {e}")
        return False


def update_alert_status(db: Session, alert_id: int, status: str) -> Alert | None:
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        return None

    alert.status = status
    db.commit()
    db.refresh(alert)

    return alert


def get_alerts_by_ticket(db: Session, ticket_id: str):
    return (
        db.query(Alert)
        .filter(Alert.ticket_id == ticket_id)
        .order_by(Alert.created_at.desc())
        .all()
    )