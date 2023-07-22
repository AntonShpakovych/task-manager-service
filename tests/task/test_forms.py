from datetime import date, timedelta
from django.test import TestCase


from task.forms import TaskCreateForm
from task.models import TaskType


class TaskCreateFormTest(TestCase):
    def setUp(self):
        self.task_data = {
            "name": "TaskName",
            "task_type": TaskType.objects.create(name="TaskTypeName"),
            "priority": 2,
            "description": "some description",
            "deadline": date.today() - timedelta(1),
        }

    def test_invalid_deadline(self):
        form = TaskCreateForm(data=self.task_data)
        self.assertFalse(form.is_valid())
