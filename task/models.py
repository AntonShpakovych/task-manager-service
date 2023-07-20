from django.conf import settings
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class TaskType(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self) -> str:
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = (
        (0, "Low"),
        (1, "Medium"),
        (2, "High"),
    )

    name = models.CharField(max_length=25)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(
        Tag,
        related_name="tasks"
    )

    def __str__(self) -> str:
        return self.name
