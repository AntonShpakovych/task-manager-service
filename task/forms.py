from datetime import date


from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from task.models import Task, TaskType, Tag


class TaskCreateForm(forms.ModelForm):
    assignees = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}),
    )

    task_type = forms.ModelChoiceField(
        queryset=TaskType.objects.all(),
        widget=forms.RadioSelect
    )

    priority = forms.ChoiceField(
        widget=forms.RadioSelect(attrs={"class": "formbold-radio"}),
        choices=Task.PRIORITY_CHOICES
    )

    class Meta:
        model = Task
        exclude = ("is_completed", )

    def clean_deadline(self):
        deadline = self.cleaned_data.get("deadline")

        if date.today() >= deadline:
            raise ValidationError("Invalid date for deadline")
        return deadline


class TaskUpdateForm(TaskCreateForm):
    class Meta(TaskCreateForm.Meta):
        exclude = tuple()
        fields = "__all__"
