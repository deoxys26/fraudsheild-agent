# FraudShield Agent

FraudShield Agent is an Agentic AI-powered fraud complaint triage system for digital banking. It helps customers submit fraud complaints and helps bank officers classify, prioritize, analyze, and track cases using AI-assisted decision support.

The project is designed for banking, fintech, and customer-support workflows where fraud complaints need to be handled quickly, consistently, and transparently.

---

## Problem Statement

Banks receive a large number of fraud-related complaints such as phishing attacks, unauthorized UPI transactions, card fraud, ATM cash-not-dispensed cases, and wrong beneficiary transfers.

In many cases, officers have to manually read the complaint, identify the fraud type, check missing information, decide priority, and update case status. This process can be slow, inconsistent, and difficult to manage at scale.

FraudShield Agent solves this by using AI to assist with complaint understanding, risk scoring, ticket creation, missing-detail detection, and officer-ready summaries.

---

## Solution Overview

FraudShield Agent provides a structured digital workflow for fraud complaint handling.

When a customer submits a complaint, the system analyzes the complaint using AI, identifies the fraud category, extracts important details, checks for missing information, assigns a severity level and risk score, and creates a complaint ticket for officers.

Officers can then view all tickets in a dashboard, filter cases, update ticket status, add notes, check alerts, review audit logs, and take action based on the AI-generated summary and recommended next steps.

The AI does not make the final decision. It assists human officers by reducing manual review time and improving case prioritization.

---

## Key Features

### Customer Side

- Submit fraud complaints digitally
- Provide customer details such as name, phone number, and account last four digits
- Describe the fraud incident in natural language
- Receive a structured complaint ticket
- Track complaint status

### Officer Side

- View all fraud complaint tickets
- Filter tickets by status, severity, and category
- View AI-generated officer summaries
- Check missing customer details
- Update complaint status
- Add officer notes
- Review alerts and audit logs
- Track case progress

### AI Features

- Fraud category detection
- Amount extraction
- Missing-detail detection
- Risk score generation
- Severity classification
- Priority reason generation
- Officer-ready summary generation
- Recommended action generation

---

## Supported Fraud Categories

The system can classify complaints into categories such as:

- Unauthorized UPI Transaction
- ATM Cash Not Dispensed
- Phishing Fraud
- Card Fraud
- Wrong Beneficiary Transfer
- Suspicious Account Activity
- Other

---

## Tech Stack

### Frontend

- React.js
- Vite
- JavaScript
- CSS / Tailwind CSS

### Backend

- Python
- FastAPI
- REST APIs
- Pydantic
- SQLAlchemy

### Database

- PostgreSQL

### AI Layer

- Gemini API
- Prompt-based complaint analysis
- JSON-based structured AI responses

### Tools

- Git
- GitHub
- VS Code
- dotenv
- Postman / Swagger UI

---

## Project Architecture

```text
Customer Portal
      |
      v
React Frontend
      |
      v
FastAPI Backend
      |
      v
AI Complaint Analysis Service
      |
      |---- Fraud Category Detection
      |---- Missing Detail Extraction
      |---- Officer Summary Generation
      |---- Recommended Action Generation
      |
      v
Risk Scoring Service
      |
      v
Ticket Service
      |
      v
PostgreSQL Database
      |
      v
Officer Dashboard
```

---

## Process Flow

1. Customer submits a fraud complaint through the frontend.
2. FastAPI receives and validates the complaint data.
3. The AI service analyzes the complaint text.
4. The system identifies fraud category, transaction amount, missing details, officer summary, and recommended action.
5. The risk service assigns a severity level and risk score.
6. A ticket is created and stored in PostgreSQL.
7. Officers view the ticket in the dashboard.
8. Officers update status, add notes, and track missing details.
9. Audit logs and alerts help maintain transparency.

---

## Folder Structure

```text
fraudshield-agent/
│
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── requirements.txt
│   ├── .env.example
│   │
│   ├── routes/
│   │   ├── complaint_routes.py
│   │   ├── health_routes.py
│   │   └── ticket_routes.py
│   │
│   ├── services/
│   │   ├── agent_service.py
│   │   ├── agent_decision_service.py
│   │   ├── audit_service.py
│   │   ├── notification_service.py
│   │   ├── policy_service.py
│   │   ├── risk_service.py
│   │   └── ticket_service.py
│   │
│   ├── models/
│   │   ├── schemas.py
│   │   └── ticket.py
│   │
│   └── policy_docs/
│
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── App.jsx
│       ├── api/
│       └── components/
│
├── .gitignore
└── README.md
```

---

## Backend Setup

### 1. Go to the backend folder

```bash
cd backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

For Windows PowerShell:

```bash
venv\Scripts\activate
```

For macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Create `.env` file

Create a `.env` file inside the `backend` folder using `.env.example`.

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fraudshield
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_USER=your_email_here
EMAIL_PASSWORD=your_email_app_password_here
```

### 6. Run the backend

```bash
uvicorn main:app --reload
```

The backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend Setup

### 1. Go to the frontend folder

```bash
cd frontend
```

### 2. Install dependencies

```bash
npm install
```

### 3. Run the frontend

```bash
npm run dev
```

The frontend will run at:

```text
http://localhost:5173
```

---

## Environment Variables

The real `.env` file should not be pushed to GitHub.

Use this format in `backend/.env.example`:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/fraudshield
GEMINI_API_KEY=your_gemini_api_key_here
EMAIL_USER=your_email_here
EMAIL_PASSWORD=your_email_app_password_here
```

---

## API Endpoints

### Health Check

```http
GET /api/health
```

Checks whether the backend server is running.

### Analyze Complaint

```http
POST /api/complaints/analyze
```

Analyzes a fraud complaint and creates a structured response.

Example request:

```json
{
  "complaint": "I clicked a fake KYC link and lost 80000 from my SBI account.",
  "customer_name": "Rahul Sharma",
  "account_last4": "1234",
  "phone": "9876543210"
}
```

Example response:

```json
{
  "ticket_id": "SBI-FRD-001",
  "category": "Phishing Fraud",
  "amount": 80000,
  "severity": "Critical",
  "risk_score": 90,
  "missing_details": ["Transaction ID", "Date and time of incident"],
  "recommended_action": "Escalate to fraud investigation team and temporarily freeze suspicious transactions.",
  "officer_summary": "Customer reported losing 80000 after clicking a fake KYC phishing link.",
  "status": "Escalated"
}
```

### Get Tickets

```http
GET /api/tickets
```

Fetches all complaint tickets.

### Update Ticket Status

```http
PATCH /api/tickets/{ticket_id}/status
```

Updates the status of a complaint ticket.

### Update Officer Note

```http
PATCH /api/tickets/{ticket_id}/officer-note
```

Adds or updates officer notes for a ticket.

---

## Risk Scoring Logic

FraudShield Agent assigns a risk score based on factors such as:

- Fraud type
- Transaction amount
- Urgency
- Missing information
- Customer impact
- Suspicious activity pattern

Example severity levels:

```text
Low       → Minor issue or low-risk complaint
Medium    → Requires officer review
High      → Serious fraud risk
Critical  → Urgent case requiring escalation
```

---

## Example Complaints

### Phishing Fraud

```text
I clicked a fake KYC update link and 80000 was debited from my account.
```

Expected output:

```text
Category: Phishing Fraud
Severity: Critical
Risk Score: High
Action: Escalate immediately
```

### ATM Cash Not Dispensed

```text
I withdrew 10000 from an ATM but cash was not dispensed and the amount was deducted.
```

Expected output:

```text
Category: ATM Cash Not Dispensed
Severity: Medium
Risk Score: Moderate
Action: Verify ATM transaction logs
```

### Unauthorized UPI Transaction

```text
A UPI transaction of 15000 happened from my account without my permission.
```

Expected output:

```text
Category: Unauthorized UPI Transaction
Severity: High
Risk Score: High
Action: Verify transaction and escalate
```

---

## Screenshots

Add screenshots in a `screenshots` folder and update this section.

```text
screenshots/
├── customer-portal.png
├── officer-dashboard.png
├── ticket-details.png
└── swagger-api.png
```

Example:

```md
![Customer Portal](screenshots/customer-portal.png)

![Officer Dashboard](screenshots/officer-dashboard.png)
```

---

## Business Value

FraudShield Agent can help banks and fintech companies by:

- Reducing manual complaint triage time
- Improving fraud complaint prioritization
- Making officer workflows more structured
- Increasing consistency in complaint handling
- Helping customers submit clearer complaints
- Supporting faster escalation of high-risk cases
- Maintaining audit logs for transparency

---

## Commercial Potential

FraudShield Agent can be offered as a B2B SaaS product for:

- Banks
- NBFCs
- Fintech companies
- Digital payment platforms
- Customer support teams
- Fraud investigation teams

Possible pricing models:

- Per officer per month
- Per complaint processed
- Enterprise API integration
- Custom deployment for banks

---

## Safety and Compliance Note

FraudShield Agent does not automatically approve, reject, refund, or settle fraud complaints.

The system only assists officers by generating summaries, risk scores, missing-detail checks, and recommended actions. Final decisions must always remain with authorized human officers.

This makes the system safer and more suitable for banking environments where human review is important.

---

## Future Improvements

- Customer and officer authentication
- Role-based access control
- OTP verification simulation
- Admin dashboard
- Analytics dashboard
- Category-wise fraud charts
- Email/SMS notification integration
- Docker Compose setup
- Unit tests and API tests
- Policy-based RAG for banking guidelines
- Deployment on cloud platforms
- Demo video and public live link

---

## GitHub Repository

```text
https://github.com/deoxys26/fraudshield-agent
```

---

## Author

**Phani M**  
B.Tech Electronics and Communication Engineering  
National Institute of Technology, Warangal  

GitHub: `deoxys26`

---

## License

This project is currently built for academic, learning, and hackathon purposes.
