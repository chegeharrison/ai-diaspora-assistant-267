def calculate_risk(intent: str, entities: dict) -> tuple[int, str]:
    score = 20
    reasons = []

    if intent == "send_money":
        score += 20
        reasons.append("Money transfer requests carry moderate operational risk.")

        amount = entities.get("amount", "").lower()
        if "15000" in amount or "20,000" in amount or "50000" in amount:
            score += 20
            reasons.append("Higher transfer amount increases risk.")

        if entities.get("urgency") == "high":
            score += 15
            reasons.append("Urgent requests increase fraud risk.")

    elif intent == "verify_document":
        score += 35
        reasons.append("Document verification has elevated fraud and legal risk.")

        if entities.get("document_type") == "land title":
            score += 20
            reasons.append("Land title checks are high-risk due to ownership disputes.")

    elif intent == "hire_service":
        score += 15
        reasons.append("Service hiring has moderate coordination risk.")

    elif intent == "get_airport_transfer":
        score += 10
        reasons.append("Airport transfer has relatively lower risk.")

    elif intent == "check_status":
        score += 5
        reasons.append("Status checks are low-risk.")

    score = min(score, 100)
    return score, " ".join(reasons)