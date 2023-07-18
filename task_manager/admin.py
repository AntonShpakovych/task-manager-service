from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from task_manager.models import Employee, TaskType, Task, Position


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("get_position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {
                    "fields": (
                        "first_name",
                        "last_name",
                        "position",
                    )
                },
            ),
        )
    )
    list_filter = UserAdmin.list_filter + ("position", )

    @admin.display(ordering='position__name', description='Position')
    def get_position(self, obj):
        return obj.position.name


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
admin.site.register(Position)
