import datetime
import pytz

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from task.models import Task, TaskType


class TaskNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=25,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "text search-input",
                "placeholder": "Searching by task name"
            }
        )
    )


class TaskTypeNameSearchForm(forms.Form):
    name = forms.CharField(
        max_length=10,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "class": "text search-input",
                "placeholder": "Searching by task type name"
            }
        )
    )


class TaskFormCreate(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    deadline = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={"type": "datetime-local"}),
        input_formats=["%Y-%m-%dT%H:%M"],
    )

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.RadioSelect
    )

    priority = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=Task.PRIORITY_CHOICES
    )

    class Meta:
        model = Task
        exclude = ("is_completed", )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")

        if datetime.datetime.now(pytz.utc) >= deadline:
            raise ValidationError("Invalid date for deadline")
        return deadline


class TaskFormUpdate(TaskFormCreate):
    class Meta(TaskFormCreate.Meta):
        exclude = tuple()
        fields = "__all__"