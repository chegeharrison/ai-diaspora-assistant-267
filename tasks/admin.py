from django.contrib import admin
from .models import Task, TaskStep, TaskMessage, StatusHistory

# Register your models here.
class TaskStepInline(admin.TabularInline):
    model = TaskStep
    extra = 1


class TaskMessageInline(admin.TabularInline):
    model = TaskMessage
    extra = 0


class StatusHistoryInline(admin.TabularInline):
    model = StatusHistory
    extra = 0
    readonly_fields = ("old_status", "new_status", "changed_at")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_code",
        "intent",
        "status",
        "risk_score",
        "employee_assignment",
        "created_at",
    )
    list_filter = ("intent", "status", "employee_assignment")
    search_fields = ("task_code", "raw_request")
    readonly_fields = ("task_code", "created_at", "updated_at")
    inlines = [TaskStepInline, TaskMessageInline, StatusHistoryInline]


@admin.register(TaskStep)
class TaskStepAdmin(admin.ModelAdmin):
    list_display = ("task", "step_number", "is_completed")
    list_filter = ("is_completed",)


@admin.register(TaskMessage)
class TaskMessageAdmin(admin.ModelAdmin):
    list_display = ("task", "channel", "created_at")
    list_filter = ("channel",)


@admin.register(StatusHistory)
class StatusHistoryAdmin(admin.ModelAdmin):
    list_display = ("task", "old_status", "new_status", "changed_at")
    list_filter = ("new_status",)
