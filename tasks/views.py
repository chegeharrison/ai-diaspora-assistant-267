from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerRequestForm
from .models import Task
from .services.task_creator import create_task_from_request
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Task, StatusHistory

# Create your views here.
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def create_task_view(request):
    if request.method == "POST":
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            raw_request = form.cleaned_data["customer_request"]

            try:
                task = create_task_from_request(raw_request)
                return redirect("task_detail", task_id=task.id)
            except Exception as e:
                logger.exception("Task creation failed")
                if settings.DEBUG:
                    form.add_error(None, f"Task creation failed: {e}")
                else:
                    form.add_error(None, "We could not process your request right now. Please try again.")
    else:
        form = CustomerRequestForm()

    return render(request, "tasks/create_task.html", {"form": form})

def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    referenced_task = None
    if task.intent == "check_status":
        requested_code = (task.entities.get("task_code") or "").strip()
        if requested_code:
            referenced_task = Task.objects.filter(task_code=requested_code).first()

    return render(
        request,
        "tasks/detail.html",
        {
            "task": task,
            "referenced_task": referenced_task,
        },
    )
    
def dashboard_view(request):
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "tasks/dashboard.html", {"tasks": tasks})


@require_POST
def update_task_status_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    new_status = request.POST.get("status", "").strip()

    valid_statuses = {"pending", "in_progress", "completed"}
    if new_status not in valid_statuses:
        return JsonResponse({"success": False, "error": "Invalid status"}, status=400)

    old_status = task.status
    if old_status != new_status:
        task.status = new_status
        task.save()

        StatusHistory.objects.create(
            task=task,
            old_status=old_status,
            new_status=new_status,
        )

    return JsonResponse(
        {
            "success": True,
            "task_id": task.id,
            "new_status": task.get_status_display(),
        }
    )