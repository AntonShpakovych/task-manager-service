from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Employee(AbstractUser):
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name="employees"
    )

    class Meta:
        verbose_name = "employee"
        verbose_name_plural = "employees"


class TaskType(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('LW', 'Lowest'),
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
        ('HG', 'Highest'),
    )

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=2,
        choices=PRIORITY_CHOICES
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
