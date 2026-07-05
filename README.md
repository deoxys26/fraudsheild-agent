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
