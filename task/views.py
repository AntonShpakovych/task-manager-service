from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from services.task_marker_query_service import TaskMarkerQueryService
from task.models import (
    Task,
    TaskType,
    Tag
)
from task.forms import (
    TaskCreateForm,
    TaskUpdateForm,
)

from simple_forms.search_by_name import SearchByNameForm
from services.task_query_service import TaskQueryService
from services.pagination_detail_service import PaginationDetailService
from custom_generic.sort_filter_search_list_view import SorterFilterListView


class TaskListView(LoginRequiredMixin, SorterFilterListView):
    model = Task
    paginate_by = 6
    searching_field = "name"
    form_class = SearchByNameForm
    service_class = TaskQueryService
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related(
        "task_type"
    ).prefetch_related("assignees").prefetch_related("tags")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskCreateForm
    success_url = reverse_lazy("task:task-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["is_task_type"] = TaskType.objects.count() >= 1
        return context


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    success_url = reverse_lazy("task:task-list")


class TaskTypeListView(LoginRequiredMixin, SorterFilterListView):
    model = TaskType
    template_name = "task/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5
    searching_field = "name"
    form_class = SearchByNameForm
    service_class = TaskMarkerQueryService
    queryset = TaskType.objects.annotate(task_count=Count("tasks"))


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task/task_type_form.html"
    success_url = reverse_lazy("task:task-type-list")


class TaskTypeDetailView(LoginRequiredMixin, generic.DetailView):
    model = TaskType
    context_object_name = "task_type"
    template_name = "task/task_type_detail.html"

    def get_queryset(self):
        return super().get_queryset().prefetch_related("tasks")


@login_required
def task_type_detail(request, pk):
    task_type_tasks = TaskType.objects.prefetch_related(
        "tasks"
    ).get(id=pk).tasks.all()

    context = PaginationDetailService(
        queryset=task_type_tasks,
        page_number=request.GET.get("page"),
        items_per_page=5
    ).generate_context()

    return render(request, "task/task_type_detail.html", context=context)


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task/task_type_confirm_delete.html"
    success_url = reverse_lazy("task:task-type-list")


class TagListView(LoginRequiredMixin, SorterFilterListView):
    model = Tag
    paginate_by = 5
    searching_field = "name"
    form_class = SearchByNameForm
    service_class = TaskMarkerQueryService
    queryset = Tag.objects.annotate(task_count=Count("tasks"))


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("task:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("task:tag-list")


@login_required
def tag_detail(request, pk):
    tag_tasks = Tag.objects.prefetch_related(
        "tasks"
    ).get(id=pk).tasks.all()

    context = PaginationDetailService(
        queryset=tag_tasks,
        page_number=request.GET.get("page"),
        items_per_page=5
    ).generate_context()

    return render(request, "task/tag_detail.html", context=context)
