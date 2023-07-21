from django.db.models import Count
from django.views.generic import ListView

from services.task_marker_query_service import TaskMarkerQueryService
from simple_forms.search_by_name import SearchByNameForm


class TaskMarkerMixin(ListView):
    """Marker: task_type or tag"""

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = SearchByNameForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        queryset = super().get_queryset().annotate(task_count=Count("tasks"))

        option = self.request.GET.get("sort")

        if TaskMarkerQueryService.is_option_valid(option):
            queryset = TaskMarkerQueryService(
                queryset=queryset,
                option=option
            ).run_query()

        form = SearchByNameForm(self.request.GET)

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset

