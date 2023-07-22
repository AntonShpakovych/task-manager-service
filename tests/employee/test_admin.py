from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from employee.models import Position


class AdminSiteTestMixin(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin", password="admin12345", email="admin@gmail.com"
        )
        self.client.force_login(self.admin_user)


class EmployeeAdminSiteTest(AdminSiteTestMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.employee = get_user_model().objects.create(
            username="Employee",
            password="Employee12345!",
            first_name="EmployeeFirstname",
            last_name="EmployeeLastname",
            position=Position.objects.create(name="DevOps"),
        )

    def test_employee_position_changelist(self):
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.employee.position)

    def test_employee_position_filter_changelist(self):
        url = reverse("admin:employee_employee_changelist")
        response = self.client.get(url)
        self.assertContains(response, "By position")

    def test_employee_position_change(self):
        url = reverse(
            "admin:employee_employee_change",
            args=[self.employee.id]
        )
        response = self.client.get(url)

        self.assertContains(response, self.employee.position)

    def test_employee_add(self):
        url = reverse("admin:employee_employee_add")
        response = self.client.get(url)
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "Position")
