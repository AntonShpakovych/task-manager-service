from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from task.models import (
    Task,
    TaskType,
    Tag
)
from task.forms import (
    TaskFormCreate,
    TaskFormUpdate,
    TaskNameSearchForm,
)

from services.task_query_service import TaskQueryService
from mixins.task_marker_mixin import TaskMarkerMixin


class TaskListView(LoginRequiredMixin, TaskMarkerMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_queryset(self):
        self.queryset = Task.objects.select_related(
            "task_type"
        ).prefetch_related("assignees")

        option = self.request.GET.get("sort")

        if TaskQueryService.is_option_valid(option):
            self.queryset = TaskQueryService(
                queryset=self.queryset,
                option=option
            ).run_query()

        form = TaskNameSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


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
    form_class = TaskFormCreate
    success_url = reverse_lazy("task:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskFormUpdate
    success_url = reverse_lazy("task:task-list")


class TaskTypeListView(LoginRequiredMixin, TaskMarkerMixin, generic.ListView):
    model = TaskType
    template_name = "task/task_type_list.html"
    context_object_name = "task_type_list"
    paginate_by = 5


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


class TagListView(LoginRequiredMixin, TaskMarkerMixin, generic.ListView):
    model = Tag
    paginate_by = 5


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


class TagDetailView(LoginRequiredMixin, generic.DetailView):
    model = Tag

    def get_queryset(self):
        return super().get_queryset().prefetch_related("tasks")
