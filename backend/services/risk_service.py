def calculate_risk_score(category: str, amount: float, complaint: str = "") -> dict:
    category_lower = category.lower()
    complaint_lower = complaint.lower()
    score = 20

    if "phishing" in category_lower:
        score += 45
    elif "unauthorized upi" in category_lower:
        score += 40
    elif "suspicious" in category_lower:
        score += 40
    elif "card" in category_lower:
        score += 30
    elif "wrong beneficiary" in category_lower:
        score += 25
    elif "atm" in category_lower:
        score += 20
    else:
        score += 10

    if amount >= 100000:
        score += 30
    elif amount >= 50000:
        score += 25
    elif amount >= 10000:
        score += 15
    elif amount >= 5000:
        score += 10
    elif amount > 0:
        score += 5

    repeated_signals = [
        "multiple",
        "repeated",
        "many",
        "several",
        "overnight",
        "debit alerts",
        "small debits",
        "unauthorized debit alerts"
    ]

    if any(signal in complaint_lower for signal in repeated_signals):
        score = max(score, 70)

    score = min(score, 100)

    if score >= 85:
        severity = "Critical"
    elif score >= 70:
        severity = "High"
    elif score >= 45:
        severity = "Medium"
    else:
        severity = "Low"

    return {
        "risk_score": score,
        "severity": severity
    }