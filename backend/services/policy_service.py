import os

POLICY_DIR = "policy_docs"


CATEGORY_TO_POLICY_FILE = {
    "Unauthorized UPI Transaction": "upi_fraud_policy.txt",
    "ATM Cash Not Dispensed": "atm_dispute_policy.txt",
    "Phishing Fraud": "phishing_response_policy.txt",
    "Card Fraud": "card_fraud_policy.txt",
    "Wrong Beneficiary Transfer": "wrong_transfer_policy.txt",
    "Suspicious Account Activity": "upi_fraud_policy.txt",
    "Other": "upi_fraud_policy.txt",
}


CATEGORY_REQUIRED_DETAILS = {
    "Unauthorized UPI Transaction": [
        "Transaction ID / UTR number",
        "Date and time of transaction",
        "Amount debited",
        "UPI app used",
        "Customer account last 4 digits",
        "Whether UPI PIN, OTP, or device access was shared",
        "Whether customer clicked any suspicious link"
    ],
    "ATM Cash Not Dispensed": [
        "ATM location or ATM ID",
        "Transaction date and time",
        "Amount debited",
        "Account last 4 digits",
        "Transaction reference number",
        "Whether receipt was generated",
        "Whether the ATM belonged to same bank or another bank"
    ],
    "Phishing Fraud": [
        "Transaction ID / UTR number",
        "Date and time of transaction",
        "Amount lost",
        "Beneficiary account or UPI ID if available",
        "Customer account last 4 digits",
        "Link/app/phone number involved",
        "Whether OTP, PIN, password, card details, or remote access was shared"
    ],
    "Card Fraud": [
        "Card last 4 digits",
        "Transaction amount",
        "Merchant name",
        "Date and time of transaction",
        "Whether card is physically with customer",
        "Whether OTP was shared",
        "Whether transaction was domestic or international"
    ],
    "Wrong Beneficiary Transfer": [
        "Transaction ID / UTR number",
        "Date and time of transfer",
        "Amount transferred",
        "Beneficiary account or UPI ID",
        "Customer account last 4 digits",
        "Whether beneficiary is known or unknown"
    ],
    "Suspicious Account Activity": [
        "Transaction ID / UTR number",
        "Date and time of suspicious activity",
        "Amount involved",
        "Customer account last 4 digits",
        "Whether customer shared OTP, PIN, password, or device access"
    ],
    "Other": [
        "Customer account last 4 digits",
        "Date and time of issue",
        "Transaction/reference number if available",
        "Amount involved if applicable"
    ]
}


def get_policy_for_category(category: str) -> str:
    filename = CATEGORY_TO_POLICY_FILE.get(category, "upi_fraud_policy.txt")
    file_path = os.path.join(POLICY_DIR, filename)

    if not os.path.exists(file_path):
        return "No specific policy document found for this category."

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def get_required_details_for_category(category: str) -> list[str]:
    return CATEGORY_REQUIRED_DETAILS.get(category, CATEGORY_REQUIRED_DETAILS["Other"])