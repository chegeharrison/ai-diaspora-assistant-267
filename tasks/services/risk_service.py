def calculate_risk(intent: str, entities: dict) -> tuple[int, str]:
    score = 20
    reasons = []

    amount = (entities.get("amount") or "").lower().replace(",", "")
    urgency = (entities.get("urgency") or "").lower()
    document_type = (entities.get("document_type") or "").lower()
    service_type = (entities.get("service_type") or "").lower()

    if intent == "send_money":
        score += 20
        reasons.append("Money transfer requests carry moderate operational risk.")

        if any(value in amount for value in ["15000", "20000", "50000", "75000", "100000"]):
            score += 20
            reasons.append("Higher transfer amount increases financial risk.")

        if urgency in ["high", "urgent", "urgently", "immediate"]:
            score += 15
            reasons.append("Urgent requests increase fraud risk.")

    elif intent == "verify_document":
        score += 35
        reasons.append("Document verification has elevated fraud and legal risk.")

        if "land" in document_type or "title" in document_type or "deed" in document_type:
            score += 20
            reasons.append("Land ownership documents require deeper legal and registry checks.")

    elif intent == "hire_service":
        score += 15
        reasons.append("Service hiring has moderate coordination risk.")

        if "lawyer" in service_type:
            score += 10
            reasons.append("Legal service requests need higher trust and verification.")

    elif intent == "get_airport_transfer":
        score += 10
        reasons.append("Airport transfer requests have relatively lower operational risk.")

    elif intent == "check_status":
        score += 5
        reasons.append("Status checks are low-risk.")

    score = min(score, 100)
    return score, " ".join(reasons)