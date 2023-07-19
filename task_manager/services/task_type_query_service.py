from task_manager.services.query_service_base import QueryServiceBase


class TaskTypeQueryService(QueryServiceBase):
    VALID_OPTIONS = {
        "quantity_task_desc": lambda queryset: queryset.order_by("-task_count"),
        "quantity_task_asc": lambda queryset: queryset.order_by("task_count"),

    }
