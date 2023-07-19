from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import Task
from task_manager.forms import TaskFormCreate, TaskFormUpdate
from task_manager.services.task_query_service import TaskQueryService


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 6

    def get_queryset(self):
        self.queryset = Task.objects.select_related("task_type").prefetch_related("assignees")

        option = self.request.GET.get("sort")

        if TaskQueryService.is_option_valid(option):
            self.queryset = TaskQueryService(self.queryset, option).run_query()
        return self.queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    queryset = Task.objects.select_related("task_type").prefetch_related("assignees")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task-manager:task-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskFormCreate
    success_url = reverse_lazy("task-manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskFormUpdate
    success_url = reverse_lazy("task-manager:task-list")
