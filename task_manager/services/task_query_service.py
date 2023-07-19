import datetime
import pytz

from django.db.models.query import QuerySet


class TaskQueryService:
    VALID_OPTIONS = {
        "priority_asc": lambda queryset: queryset.order_by("priority"),
        "priority_desc": lambda queryset: queryset.order_by("-priority"),
        "deadline_failed": lambda queryset: queryset.filter(
            deadline__lte=datetime.datetime.now(pytz.utc)
        ),
        "in_progress": lambda queryset: queryset.filter(
            is_completed=False,
            deadline__gt=datetime.datetime.now(pytz.utc)
        ),
        "completed": lambda queryset: queryset.filter(
            is_completed=True
        ),
        "deadline_desc": lambda queryset: queryset.order_by("-deadline"),
        "deadline_asc": lambda queryset: queryset.order_by("deadline")
    }

    def __init__(self, queryset: QuerySet, option: str) -> None:
        self.option = option
        self.queryset = queryset

    def run_query(self) -> QuerySet:
        return TaskQueryService.VALID_OPTIONS[self.option](self.queryset)

    @classmethod
    def is_option_valid(cls, option) -> bool:
        return option in TaskQueryService.VALID_OPTIONS
