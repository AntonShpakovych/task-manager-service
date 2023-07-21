import datetime
import pytz

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.views import generic

from employee.forms import (
    EmployeeUsernameSearchForm,
    EmployeeCreateForm,
    EmployeeUpdateForm,
)
from employee.models import (
    Employee,
    Position
)


from services.position_query_service import PositionQueryService
from simple_forms.search_by_name import SearchByNameForm
from task.models import Task


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


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        name = self.request.GET.get("name", "")
        context["search_form"] = SearchByNameForm(
            initial={"name": name}
        )

        return context

    def get_queryset(self):
        self.queryset = Position.objects.annotate(
            employee_count=Count("employees")
        )

        option = self.request.GET.get("sort")

        if PositionQueryService.is_option_valid(option):
            self.queryset = PositionQueryService(
                queryset=self.queryset,
                option=option
            ).run_query()

        form = SearchByNameForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )

        return self.queryset


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
