import re


def extract_intent_and_entities(user_text: str) -> dict:
    text = user_text.lower()

    result = {
        "intent": "check_status",
        "entities": {},
    }

    if "send" in text and ("kes" in text or "money" in text):
        result["intent"] = "send_money"

        amount_match = re.search(r"(kes\s?[\d,]+)", user_text, re.IGNORECASE)
        if amount_match:
            result["entities"]["amount"] = amount_match.group(1)

        if "mother" in text:
            result["entities"]["recipient"] = "mother"

        if "urgently" in text or "urgent" in text:
            result["entities"]["urgency"] = "high"

        if "kisumu" in text:
            result["entities"]["location"] = "Kisumu"

    elif "clean" in text or "cleaner" in text:
        result["intent"] = "hire_service"
        result["entities"]["service_type"] = "cleaning"

        if "westlands" in text:
            result["entities"]["location"] = "Westlands"

        if "friday" in text:
            result["entities"]["schedule"] = "Friday"

    elif "verify" in text and ("title" in text or "certificate" in text or "id" in text):
        result["intent"] = "verify_document"

        if "title" in text:
            result["entities"]["document_type"] = "land title"

        if "karen" in text:
            result["entities"]["location"] = "Karen"

    elif "airport" in text or "pickup" in text or "transfer" in text:
        result["intent"] = "get_airport_transfer"

    elif "status" in text or "track" in text or "follow up" in text:
        result["intent"] = "check_status"

    return result