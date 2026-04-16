from tasks.models import Task, StatusHistory
from .ai_service import extract_intent_and_entities
from .risk_service import calculate_risk
from .assignment_service import assign_employee_team


def create_task_from_request(raw_request: str) -> Task:
    ai_result = extract_intent_and_entities(raw_request)

    intent = ai_result["intent"]
    entities = ai_result["entities"]

    risk_score, risk_reason = calculate_risk(intent, entities)
    employee_assignment = assign_employee_team(intent)

    task = Task.objects.create(
        raw_request=raw_request,
        intent=intent,
        entities=entities,
        risk_score=risk_score,
        risk_reason=risk_reason,
        employee_assignment=employee_assignment,
        status="pending",
    )

    StatusHistory.objects.create(
        task=task,
        old_status="",
        new_status="pending",
    )

    return task