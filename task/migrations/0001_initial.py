# Generated by Django 4.2.3 on 2023-07-20 15:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=25)),
                ("description", models.TextField()),
                ("deadline", models.DateTimeField()),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "priority",
                    models.IntegerField(
                        choices=[(0, "Low"), (1, "Medium"), (2, "High")]
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "assignees",
                    models.ManyToManyField(
                        related_name="tasks", to=settings.AUTH_USER_MODEL
                    ),
                ),
                (
                    "task_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="task.tasktype",
                    ),
                ),
            ],
        ),
    ]