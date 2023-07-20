import datetime
import pytz

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from task.models import Task

from employee.forms import (
    EmployeeUsernameSearchForm,
    EmployeeCreateForm,
    EmployeeUpdateForm
)
from employee.models import Employee


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
