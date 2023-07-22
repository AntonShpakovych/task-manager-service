from django.contrib.auth import get_user_model

from employee.forms import EmployeeCreateForm
from django.test import TestCase

from employee.models import Position


class EmployeeCreateFormTest(TestCase):
    def setUp(self):
        self.employee_data = {
            "username": "Bob4ik123",
            "password1": "Bobapass123!",
            "password2": "Bobapass123!",
            "first_name": "Bob",
            "last_name": "Bambuko",
            "position": Position.objects.create(name="DevOps"),
            "email": "bob4a@gmail.com",
        }

    def test_valid_data(self):
        form = EmployeeCreateForm(data=self.employee_data)

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, self.employee_data)
        form.save()
        self.assertIsNotNone(
            get_user_model().objects.get(
                username=self.employee_data["username"]
            )
        )

    def test_without_first_name(self):
        self.employee_data["first_name"] = ""

        form = EmployeeCreateForm(data=self.employee_data)

        self.assertFalse(form.is_valid())

    def test_without_last_name(self):
        self.employee_data["last_name"] = ""

        form = EmployeeCreateForm(data=self.employee_data)

        self.assertFalse(form.is_valid())

    def test_without_email(self):
        self.employee_data["email"] = ""

        form = EmployeeCreateForm(data=self.employee_data)

        self.assertFalse(form.is_valid())

    def test_email_already_exists(self):
        get_user_model().objects.create(
            username="OldEmployee",
            first_name="Oldname",
            last_name="nameOld",
            email=self.employee_data["email"],
            position=self.employee_data["position"],
            password="Password123q",
        )

        form = EmployeeCreateForm(data=self.employee_data)

        self.assertFalse(form.is_valid())
