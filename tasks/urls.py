from django.urls import path
from .views import create_task_view, task_detail_view, dashboard_view, update_task_status_view

urlpatterns = [
    path("create/", create_task_view, name="create_task"),
    path("<int:task_id>/", task_detail_view, name="task_detail"),
    path("dashboard/", dashboard_view, name="task_dashboard"),
    path("<int:task_id>/update-status/", update_task_status_view, name="update_task_status"),
]