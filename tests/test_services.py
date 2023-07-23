from datetime import date, timedelta

from django.db.models import Count
from django.test import TestCase

from services.pagination_detail_service import PaginationDetailService
from task.models import Tag, Task, TaskType

from services.query_service_base import QueryServiceBase
from services.task_marker_query_service import TaskMarkerQueryService


class QueryServiceBaseTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(
            name="task_with_tag",
            priority=2,
            description="some desc",
            deadline=date.today() + timedelta(1),
            task_type=TaskType.objects.create(name="Development"),
        )
        self.service = QueryServiceBase
        self.service.VALID_OPTIONS = TaskMarkerQueryService.VALID_OPTIONS

    def test_run_query(self):
        Tag.objects.create(name="Tag without task")
        tag_with_task = Tag.objects.create(name="Refactoring")
        self.task.tags.add(tag_with_task)

        self.service = self.service(
            option="quantity_task_desc",
            queryset=Tag.objects.prefetch_related("tasks").annotate(
                task_count=Count("tasks")
            ),
        )

        response = self.service.run_query()

        self.assertEqual(response.first(), tag_with_task)


class PaginationDetailServiceTest(TestCase):
    def setUp(self):
        for i in range(10):
            Tag.objects.create(name=f"Tag{i}")
        self.service = PaginationDetailService(
            queryset=Tag.objects.all(), page_number=1, items_per_page=5
        )

    def test_generate_context(self):
        context = self.service.generate_context()

        self.assertTrue("page_obj" in context)
        self.assertTrue("is_paginated" in context)
        self.assertTrue("paginator" in context)
        self.assertEqual(context["page_obj"].number, self.service.page_number)
        self.assertEqual(context["paginator"].num_pages, 2)
