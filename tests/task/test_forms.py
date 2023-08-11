from datetime import date, timedelta
from django.test import TestCase


from task.forms import TaskCreateForm
from task.models import TaskType, Task


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

    def test_valid_deadline(self):
        self.task_data["deadline"] = date.today() + timedelta(1)
        form = TaskCreateForm(data=self.task_data)
        self.assertTrue(form.is_valid())
        form.save()

        self.assertEqual(
            Task.objects.get(id=1).name,
            self.task_data["name"]
        )
