import datetime
import pytz

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic

from task.models import Task

from employee.forms import (
    EmployeeUsernameSearchForm,
    EmployeeCreateForm,
    EmployeeUpdateForm,
)
from employee.models import (
    Employee,
    Position
)

from mixins.task_marker_mixin import SorterFilterMixin
from services.position_query_service import PositionQueryService
from simple_forms.search_by_name import SearchByNameForm


class EmployeeListView(LoginRequiredMixin, SorterFilterMixin, generic.ListView):
    model = Employee
    paginate_by = 6
    form_class = EmployeeUsernameSearchForm
    searching_field = "username"
    queryset = Employee.objects.select_related("position")


class EmployeeCreateView(LoginRequiredMixin, generic.CreateView):
    model = Employee
    form_class = EmployeeCreateForm
    success_url = reverse_lazy("employee:employee-list")


class EmployeeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Employee
    success_url = reverse_lazy("employee:employee-list")


class EmployeeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    success_url = reverse_lazy("employee:employee-list")


class EmployeeDetailView(LoginRequiredMixin, generic.DetailView):
    model = Employee

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee = context["object"]
        employee_tasks = Task.objects.prefetch_related("assignees").filter(
            assignees__id=employee.id
        )

        employee_tasks_with_status = {
            "completed": employee_tasks.filter(
                is_completed=True
            ),
            "failed": employee_tasks.filter(
                deadline__lte=datetime.datetime.now(pytz.utc),
                is_completed=False
            ),
            "in progress": employee_tasks.filter(
                is_completed=False,
                deadline__gt=datetime.datetime.now(pytz.utc)
            )
        }

        context["task_statuses"] = employee_tasks_with_status

        return context


class PositionListView(LoginRequiredMixin, SorterFilterMixin, generic.ListView):
    model = Position
    queryset = Position.objects.annotate(employee_count=Count("employees"))
    form_class = SearchByNameForm
    searching_field = "name"
    service_class = PositionQueryService


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("employee:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("employee:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("employee:position-list")
