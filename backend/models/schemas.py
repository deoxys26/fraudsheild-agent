from pydantic import BaseModel

from enum import Enum
from datetime import datetime
from typing import List, Optional, Dict


class TicketStatus(str, Enum):
    open = "Open"
    in_review = "In Review"
    escalated = "Escalated"
    resolved = "Resolved"
    rejected = "Rejected"


class TicketDetailsUpdate(BaseModel):
    collected_details: Dict[str, str]


class ComplaintRequest(BaseModel):
    complaint: str
    customer_name: Optional[str] = None
    account_last4: Optional[str] = None
    phone: Optional[str] = None

class OfficerNoteUpdate(BaseModel):
    note: str

class ComplaintAnalysis(BaseModel):
    category: str
    amount: Optional[float] = 0
    missing_details: List[str]
    recommended_action: str
    officer_summary: str
    priority_reason: str


class FinalComplaintResponse(BaseModel):
    ticket_id: str

    customer_name: Optional[str] = None
    account_last4: Optional[str] = None
    phone: Optional[str] = None

    original_complaint: str
    category: str
    amount: Optional[float]
    severity: str
    risk_score: int
    priority_reason: str
    missing_details: List[str]
    recommended_action: str
    officer_summary: str
    status: str

    officer_note: Optional[str] = None

    created_at: datetime
    updated_at: Optional[datetime] = None
    collected_details: Optional[Dict[str, str]] = None

    model_config = {
        "from_attributes": True
    }

class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketResponse(BaseModel):
    ticket_id: str

    customer_name: Optional[str] = None
    account_last4: Optional[str] = None
    phone: Optional[str] = None

    created_at: datetime
    updated_at: Optional[datetime] = None
    status: str

    original_complaint: str
    category: str
    amount: Optional[float]
    severity: str
    risk_score: int
    priority_reason: str
    missing_details: List[str]
    recommended_action: str
    officer_summary: str

    officer_note: Optional[str] = None
    collected_details: Optional[Dict[str, str]] = None

    model_config = {
        "from_attributes": True
    }