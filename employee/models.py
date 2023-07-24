from django.contrib.auth.models import AbstractUser
from django.db import models

from employee.managers import CustomUserManager


class Position(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Employee(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        related_name="employees",
    )
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ["position"]
