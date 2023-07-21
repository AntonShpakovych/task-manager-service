from django.core.paginator import Paginator


class PaginationDetailService:
    def __init__(self, queryset, page_number, items_per_page):
        self.queryset = queryset
        self.page_number = page_number
        self.items_per_page = items_per_page

    def generate_context(self):
        paginator = Paginator(
            self.queryset,
            self.items_per_page
        )

        page_obj = paginator.get_page(self.page_number)

        is_paginated = page_obj.has_other_pages()

        context = {
            "page_obj": page_obj,
            "is_paginated": is_paginated,
            "paginator": paginator,
        }

        return context
