import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

from models.schemas import ComplaintAnalysis
from services.policy_service import (
    get_policy_for_category,
    get_required_details_for_category
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is missing in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


VALID_CATEGORIES = [
    "Unauthorized UPI Transaction",
    "ATM Cash Not Dispensed",
    "Phishing Fraud",
    "Card Fraud",
    "Wrong Beneficiary Transfer",
    "Suspicious Account Activity",
    "Other"
]


def extract_json(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if not match:
        raise ValueError("Could not extract valid JSON from AI response")

    return json.loads(match.group())


def normalize_category(category: str) -> str:
    category_lower = category.lower()

    if "phishing" in category_lower or "kyc" in category_lower or "link" in category_lower:
        return "Phishing Fraud"

    if "upi" in category_lower and "unauthorized" in category_lower:
        return "Unauthorized UPI Transaction"

    if "atm" in category_lower:
        return "ATM Cash Not Dispensed"

    if "card" in category_lower:
        return "Card Fraud"

    if "wrong" in category_lower or "beneficiary" in category_lower:
        return "Wrong Beneficiary Transfer"

    if "suspicious" in category_lower or "multiple" in category_lower:
        return "Suspicious Account Activity"

    if category in VALID_CATEGORIES:
        return category

    return "Other"


def classify_complaint(complaint: str) -> dict:
    prompt = f"""
Classify this banking complaint.

Return ONLY valid JSON.
Do not use markdown.
Do not wrap JSON in triple backticks.

Complaint:
{complaint}

Return JSON:
{{
  "category": "Unauthorized UPI Transaction / ATM Cash Not Dispensed / Phishing Fraud / Card Fraud / Wrong Beneficiary Transfer / Suspicious Account Activity / Other",
  "amount": 0
}}

Rules:
- Extract amount if present.
- If complaint mentions fake KYC link, suspicious link, OTP sharing, remote app, or social engineering, category must be Phishing Fraud.
- If complaint mentions ATM cash not dispensed but amount debited, category must be ATM Cash Not Dispensed.
- If complaint mentions unauthorized UPI debit, category must be Unauthorized UPI Transaction.
- If complaint mentions card transaction not done by customer, category must be Card Fraud.
- If complaint mentions money sent to wrong UPI ID or wrong account, category must be Wrong Beneficiary Transfer.
- If no amount is found, amount must be 0.
"""

    response = model.generate_content(prompt)

    if not response.text:
        raise ValueError("Empty classification response from Gemini")

    data = extract_json(response.text)

    data["category"] = normalize_category(data.get("category", "Other"))
    data["amount"] = float(data.get("amount", 0) or 0)

    return data


def analyze_complaint_with_ai(complaint: str) -> ComplaintAnalysis:
    classification = classify_complaint(complaint)

    category = classification["category"]
    amount = classification["amount"]

    policy_text = get_policy_for_category(category)
    required_details = get_required_details_for_category(category)

    prompt = f"""
You are FraudShield Agent, an AI assistant for banking fraud complaint triage.

You must analyze the complaint using the provided banking policy.
Return ONLY valid JSON.
Do not use markdown.
Do not wrap JSON in triple backticks.

Complaint:
{complaint}

Detected Category:
{category}

Detected Amount:
{amount}

Relevant Banking Policy:
{policy_text}

Required Missing Details From Policy:
{required_details}

Return JSON in this exact format:
{{
  "category": "{category}",
  "amount": {amount},
  "missing_details": [],
  "recommended_action": "short action for bank staff based only on policy",
  "officer_summary": "short officer-ready summary",
  "priority_reason": "short reason based only on complaint amount, complaint type, and provided policy"
}}

Rules:
- Use the detected category exactly.
- Use the detected amount exactly.
- Do not create your own missing details.
- Missing details will be filled by backend policy rules.
- Recommended action must be based only on the relevant banking policy.
- Priority reason must be based only on the complaint and policy text.
- Do not mention timelines, penalties, regulations, RBI rules, or legal requirements unless they are explicitly present in the provided policy.
- Do not add facts that are not present in the policy text.
- Do not give legal advice.
- Do not reveal internal fraud detection logic.
- Keep the officer summary short and professional.
"""

    response = model.generate_content(prompt)

    if not response.text:
        raise ValueError("Empty analysis response from Gemini")

    data = extract_json(response.text)

    data["category"] = category
    data["amount"] = amount
    data["missing_details"] = required_details

    return ComplaintAnalysis(**data)