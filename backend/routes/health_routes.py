from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="/api/health",
    tags=["Health"]
)


@router.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "FraudShield Agent API",
        "timestamp": datetime.now().isoformat(timespec="seconds")
    }