from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime



from database import Base



class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, unique=True, index=True, nullable=False)
    customer_name = Column(String, nullable=True)
    account_last4 = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    officer_note = Column(Text, nullable=True)

    original_complaint = Column(Text, nullable=False)
    category = Column(String, nullable=False)
    amount = Column(Float, default=0)

    severity = Column(String, nullable=False)
    risk_score = Column(Integer, nullable=False)
    priority_reason = Column(Text, nullable=False)

    missing_details = Column(JSON, nullable=False)
    missing_details = Column(JSON, nullable=False)
    collected_details = Column(JSON, nullable=True)
    recommended_action = Column(Text, nullable=False)
    recommended_action = Column(Text, nullable=False)
    officer_summary = Column(Text, nullable=False)

    status = Column(String, default="Open")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    audit_logs = relationship("AuditLog", back_populates="ticket", cascade="all, delete")
    alerts = relationship("Alert", back_populates="ticket", cascade="all, delete")
    collected_details = Column(JSON, nullable=True)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, ForeignKey("tickets.ticket_id"), nullable=False)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="audit_logs")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, ForeignKey("tickets.ticket_id"), nullable=False)
    alert_type = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String, default="Pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("Ticket", back_populates="alerts")