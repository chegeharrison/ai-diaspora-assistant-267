from tasks.models import Task, StatusHistory, TaskStep, TaskMessage
from .ai_service import analyze_customer_request, generate_task_messages
from .risk_service import calculate_risk
from .assignment_service import assign_employee_team


def create_task_from_request(raw_request: str) -> Task:
    ai_result = analyze_customer_request(raw_request)

    intent = ai_result["intent"]
    entities = ai_result["entities"]
    steps = ai_result["steps"]

    referenced_task = None
    actual_status = ""

    if intent == "check_status":
        requested_code = (entities.get("task_code") or "").strip()
        if requested_code:
            referenced_task = Task.objects.filter(task_code=requested_code).first()
            if referenced_task:
                actual_status = referenced_task.get_status_display()
            else:
                actual_status = "Task not found"

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
            description=step_text,
        )

    messages = generate_task_messages(
        raw_request=raw_request,
        task_code=task.task_code,
        intent=task.intent,
        entities=task.entities,
        risk_score=task.risk_score,
        employee_assignment=task.employee_assignment,
        actual_status=actual_status,
        referenced_task_code=(entities.get("task_code") or ""),
    )

    for channel, content in messages.items():
        TaskMessage.objects.create(
            task=task,
            channel=channel,
            content=content,
        )

    return task