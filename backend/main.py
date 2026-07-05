from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from models import db_models

from routes.complaint_routes import complaint_router
from routes.ticket_routes import router as ticket_router
from routes.health_routes import router as health_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FraudShield Agent API",
    description="Agentic AI backend for banking fraud complaint triage",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {
        "message": "FraudShield Agent API is running",
        "docs": "/docs",
        "health": "/api/health"
    }


app.include_router(health_router)
app.include_router(complaint_router)
app.include_router(ticket_router)