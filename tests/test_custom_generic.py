from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from employee.models import Position
from task.models import Tag, Task, TaskType

from simple_forms.search_by_name import SearchByNameForm


class SorterFilterSearchListView(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="task_with_tag",
            priority=2,
            description="some desc",
            deadline=date.today() - timedelta(1),
            task_type=TaskType.objects.create(name="Development"),
        )
        self.client = Client()
        self.employee = get_user_model().objects.create(
            username="Employee",
            password="Employee12345!",
            first_name="EmployeeFirstname",
            last_name="EmployeeLastname",
            position=Position.objects.create(name="DevOps"),
        )
        self.client.force_login(self.employee)

    def test_get_context_data(self):
        url = reverse("task:tag-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("search_form", response.context)
        self.assertIsInstance(
            response.context["search_form"],
            SearchByNameForm
        )

    def test_get_queryset_filtering(self):
        Tag.objects.create(name="Design")
        tag_which_we_searching = Tag.objects.create(name="Development")

        url = reverse("task:tag-list") + "?name=vel"
        response = self.client.get(url)
        self.assertContains(response, tag_which_we_searching.name)

    def test_get_queryset_sorting_asc(self):
        tag_without_task = Tag.objects.create(name="Some tag")
        tag_with_task = Tag.objects.create(name="Refactoring")
        self.task.tags.add(tag_with_task)

        url = reverse("task:tag-list") + "?sort=quantity_task_asc"
        response = self.client.get(url)
        self.assertEqual(
            response.context["tag_list"].first(),
            tag_without_task
        )

    def test_get_queryset_sorting_desc(self):
        Tag.objects.create(name="Some tag")
        tag_with_task = Tag.objects.create(name="Refactoring")
        self.task.tags.add(tag_with_task)

        url = reverse("task:tag-list") + "?sort=quantity_task_desc"
        response = self.client.get(url)
        self.assertEqual(response.context["tag_list"].first(), tag_with_task)
