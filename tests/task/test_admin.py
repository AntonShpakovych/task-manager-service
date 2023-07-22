import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task.models import TaskType, Task


class AdminSiteTestMixin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin12345", email="admin@gmail.com"
        )
        self.client.force_login(self.admin_user)


class TaskAdminSiteTest(AdminSiteTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        for i in range(2):
            self.task = Task.objects.create(
                name=f"Task name{i}",
                task_type=TaskType.objects.create(name=f"Design{i}"),
                priority=1,
                description="somedescription",
                deadline=datetime.datetime.now() + datetime.timedelta(days=1),
            )

    def test_task_filter_changelist(self):
        url = reverse("admin:task_task_changelist")
        response = self.client.get(url)
        self.assertContains(response, "By priority")
        self.assertContains(response, "By task type")
        self.assertContains(response, "By is completed")
