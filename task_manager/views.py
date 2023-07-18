from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic

from task_manager.models import Task


# @login_required
# def index(request):
#     return render(request, "task_manager/index.html")


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task

