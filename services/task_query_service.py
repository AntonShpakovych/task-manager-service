import datetime
import pytz

from services.query_service_base import QueryServiceBase


class TaskQueryService(QueryServiceBase):
    VALID_OPTIONS = {
        "priority_asc": lambda queryset: queryset.order_by("priority"),
        "priority_desc": lambda queryset: queryset.order_by("-priority"),
        "deadline_failed": lambda queryset: queryset.filter(
            deadline__lte=datetime.datetime.now(pytz.utc),
            is_completed=False
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
