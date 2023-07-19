from django.urls import path

from task_manager.views import (
    TaskListView,
    TaskDetailView,
    TaskDeleteView,
    TaskCreateView, TaskUpdateView
)


urlpatterns = [
    path(
        "",
        TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "<int:pk>/detail/",
        TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "<int:pk>/delete/",
        TaskDeleteView.as_view(),
        name="task-delete"
    ),
    path(
        "<int:pk>/update/",
        TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "create/",
        TaskCreateView.as_view(),
        name="task-create"
    ),
]

app_name = "task_manager"
