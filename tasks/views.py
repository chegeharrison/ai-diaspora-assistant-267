from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerRequestForm
from .models import Task
from .services.task_creator import create_task_from_request

# Create your views here.
def create_task_view(request):
    if request.method == "POST":
        form = CustomerRequestForm(request.POST)
        if form.is_valid():
            raw_request = form.cleaned_data["customer_request"]

            try:
                task = create_task_from_request(raw_request)
                return redirect("task_detail", task_id=task.id)
            except Exception:
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