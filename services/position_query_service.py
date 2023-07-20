from services.query_service_base import QueryServiceBase


class PositionQueryService(QueryServiceBase):
    VALID_OPTIONS = {
        "quantity_employee_desc": lambda queryset: queryset.order_by("-employee_count"),
        "quantity_employee_asc": lambda queryset: queryset.order_by("employee_count"),

    }
