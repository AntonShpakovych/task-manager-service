from django.views.generic import ListView


class SorterFilterListView(ListView):
    searching_field = None
    form_class = None
    service_class = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search_param = self.request.GET.get(self.searching_field, "")
        context["search_form"] = self.form_class(
            initial={f"{self.searching_field}": search_param}
        )

        return context

    def get_queryset(self):
        queryset = self.queryset

        option = self.request.GET.get("sort")

        if self.service_class and self.service_class.is_option_valid(option):
            queryset = self.service_class(
                queryset=queryset,
                option=option
            ).run_query()

        form = self.form_class(self.request.GET)

        if form.is_valid():
            lookup = f"{self.searching_field}__icontains"
            search_filter_query = {
                lookup: form.cleaned_data[self.searching_field]
            }
            return queryset.filter(**search_filter_query)

        return queryset
