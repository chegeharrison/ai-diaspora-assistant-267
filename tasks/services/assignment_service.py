def assign_employee_team(intent: str) -> str:
    if intent == "send_money":
        return "finance"
    if intent == "hire_service":
        return "operations"
    if intent == "verify_document":
        return "legal"
    if intent == "get_airport_transfer":
        return "operations"
    return "customer_support"