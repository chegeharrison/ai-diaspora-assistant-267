from django.urls import path
from .views import create_task_view, task_detail_view

urlpatterns = [
    path("create/", create_task_view, name="create_task"),
    path("<int:task_id>/", task_detail_view, name="task_detail"),
]