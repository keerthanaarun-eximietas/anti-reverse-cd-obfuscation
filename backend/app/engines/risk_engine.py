
def calculate_risk(transaction):
    """
    Calculate a transaction risk score using deterministic rules.

    Maximum possible score: 90
    """

    score = 0
    reasons = []

    # Rule 1: Large transaction amount
    if transaction["amount"] >= 50000:
        score += 30
        reasons.append("High transaction amount")

    # Rule 2: Transaction country differs from account country
    if transaction["country"] != transaction["account_country"]:
        score += 25
        reasons.append("Transaction from a different country")

    # Rule 3: Multiple failed attempts
    if transaction["failed_attempts"] >= 3:
        score += 20
        reasons.append("Multiple failed transaction attempts")

    # Rule 4: Newly created account
    if transaction["account_age_days"] < 7:
        score += 15
        reasons.append("Account is less than 7 days old")

    # Determine the final decision
    if score >= 70:
        decision = "REJECT"
        risk_level = "HIGH"
    elif score >= 30:
        decision = "REVIEW"
        risk_level = "MEDIUM"
    else:
        decision = "APPROVE"
        risk_level = "LOW"

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "decision": decision,
        "reasons": reasons,
    }
