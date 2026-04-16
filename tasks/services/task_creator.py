from tasks.models import Task, StatusHistory, TaskStep, TaskMessage
from .ai_service import analyze_customer_request
from .risk_service import calculate_risk
from .assignment_service import assign_employee_team


def create_task_from_request(raw_request: str) -> Task:
    ai_result = analyze_customer_request(raw_request)

    intent = ai_result.get("intent", "check_status")
    entities = ai_result.get("entities", {})
    steps = ai_result.get("steps", [])
    messages = ai_result.get("messages", {})

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

    for index, step_text in enumerate(steps, start=1):
        TaskStep.objects.create(
            task=task,
            step_number=index,
            description=step_text
        )

    for channel in ["whatsapp", "email", "sms"]:
        content = messages.get(channel, "").strip()
        if content:
            TaskMessage.objects.create(
                task=task,
                channel=channel,
                content=content
            )

    return task