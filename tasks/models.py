from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class Task(models.Model):
    INTENT_CHOICES = [
        ("send_money", "Send Money"),
        ("get_airport_transfer", "Get Airport Transfer"),
        ("hire_service", "Hire Service"),
        ("verify_document", "Verify Document"),
        ("check_status", "Check Status"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    ASSIGNMENT_CHOICES = [
        ("finance", "Finance Team"),
        ("operations", "Operations Team"),
        ("legal", "Legal Team"),
        ("customer_support", "Customer Support"),
    ]

    task_code = models.CharField(max_length=20, unique=True, blank=True)
    raw_request = models.TextField()
    intent = models.CharField(max_length=50, choices=INTENT_CHOICES)
    entities = models.JSONField(default=dict, blank=True)

    risk_score = models.PositiveIntegerField(default=0)
    risk_reason = models.TextField(blank=True)

    employee_assignment = models.CharField(
        max_length=50,
        choices=ASSIGNMENT_CHOICES,
        default="customer_support"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.task_code:
            self.task_code = f"VNG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_code} - {self.intent}"


class TaskStep(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="steps")
    step_number = models.PositiveIntegerField()
    description = models.TextField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["step_number"]
        unique_together = ("task", "step_number")

    def __str__(self):
        return f"{self.task.task_code} - Step {self.step_number}"


class TaskMessage(models.Model):
    CHANNEL_CHOICES = [
        ("whatsapp", "WhatsApp"),
        ("email", "Email"),
        ("sms", "SMS"),
    ]

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="messages")
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("task", "channel")

    def __str__(self):
        return f"{self.task.task_code} - {self.channel}"


class StatusHistory(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="status_history")
    old_status = models.CharField(max_length=20, blank=True)
    new_status = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.task_code} - {self.old_status} to {self.new_status}"
