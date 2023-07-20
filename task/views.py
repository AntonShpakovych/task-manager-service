from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic

from task.models import (
    Task,
    TaskType,
)
from task.forms import (
    TaskFormCreate,
    TaskFormUpdate,
    TaskNameSearchForm,
    TaskTypeNameSearchForm,
)
from services.task_query_service import TaskQueryService
from services.task_type_query_service import TaskTypeQueryService


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        self.queryset = Task.objects.select_related("task_type").prefetch_related("assignees")

        option = self.request.GET.get("sort")

        if TaskQueryService.is_option_valid(option):
            self.queryset = TaskQueryService(self.queryset, option).run_query()

        form = TaskNameSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task:task-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskFormCreate
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskFormUpdate
    success_url = reverse_lazy("task:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = TaskTypeNameSearchForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        self.queryset = TaskType.objects.annotate(task_count=Count("tasks"))

        option = self.request.GET.get("sort")

        if TaskTypeQueryService.is_option_valid(option):
            self.queryset = TaskTypeQueryService(self.queryset, option).run_query()

        form = TaskTypeNameSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


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


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task/task_type_confirm_delete.html"
    success_url = reverse_lazy("task:task-type-list")
