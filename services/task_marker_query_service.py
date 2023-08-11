from services.query_service_base import QueryServiceBase


class TaskMarkerQueryService(QueryServiceBase):
    """Marker: task_type or tag"""

    VALID_OPTIONS = {
        "quantity_task_desc": lambda queryset: queryset.order_by(
            "-task_count"
        ),
        "quantity_task_asc": lambda queryset: queryset.order_by(
            "task_count"
        ),
    }
