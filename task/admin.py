from django.contrib import admin
from task.models import TaskType, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "deadline",
        "is_completed",
        "priority",
        "task_type",
        "created_at"
    )

    list_filter = ("priority", "task_type", "is_completed")


admin.site.register(TaskType)
