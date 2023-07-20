from django.db.models.query import QuerySet


class QueryServiceBase:
    VALID_OPTIONS = {}

    def __init__(self, queryset: QuerySet, option: str) -> None:
        self.option = option
        self.queryset = queryset

    def run_query(self) -> QuerySet:
        return self.VALID_OPTIONS[self.option](self.queryset)

    @classmethod
    def is_option_valid(cls, option) -> bool:
        return option in cls.VALID_OPTIONS
