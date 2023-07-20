import datetime
import pytz

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic

from task_manager.models import (
    Task,
    TaskType,
    Employee
)
from task_manager.forms import (
    TaskFormCreate,
    TaskFormUpdate,
    TaskNameSearchForm,
    TaskTypeNameSearchForm,
    EmployeeCreateForm,
    EmployeeUpdateForm,
    EmployeeUsernameSearchForm
)
from task_manager.services.task_query_service import TaskQueryService
from task_manager.services.task_type_query_service import TaskTypeQueryService


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
    success_url = reverse_lazy("task-manager:task-list")


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskFormCreate
    success_url = reverse_lazy("task-manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskFormUpdate
    success_url = reverse_lazy("task-manager:task-list")


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    template_name = "task_manager/task_type_list.html"
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
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task-manager:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    template_name = "task_manager/task_type_form.html"
    success_url = reverse_lazy("task-manager:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    template_name = "task_manager/task_type_confirm_delete.html"
    success_url = reverse_lazy("task-manager:task-type-list")


class EmployeeListView(LoginRequiredMixin, generic.ListView):
    model = Employee
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.GET.get("username", "")
        context["search_form"] = EmployeeUsernameSearchForm(
            initial={"username": username}
        )

        return context

    def get_queryset(self):
        self.queryset = Employee.objects.select_related("position")

        form = EmployeeUsernameSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )

        return self.queryset


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    success_url = reverse_lazy("task-manager:employee-list")


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("task-manager:employee-list")


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("task-manager:employee-list")


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tasks = Task.objects.prefetch_related("assignees")
        employee = context["object"]

        employee_tasks_with_status = {
            "completed": tasks.filter(
                assignees__id=employee.id, is_completed=True
            ),
            "failed": tasks.filter(
                assignees__id=employee.id,
                deadline__lte=datetime.datetime.now(pytz.utc),
                is_completed=False
            ),
            "in progress": tasks.filter(
                assignees__id=employee.id,
                is_completed=False,
                deadline__gt=datetime.datetime.now(pytz.utc)
            )
        }

        context["task_statuses"] = employee_tasks_with_status

        return context
