"""Custom forms for app_plan."""

from typing import Any

from django import forms

from app_plan.models import ProjectTeamMember, Stage, Task


class StageInlineForm(forms.ModelForm):
    """StageInline admin model form."""

    class Meta:
        """Form metadata."""

        model = Stage
        fields = "__all__"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Redefine main logic of form displaying."""
        # извлекаем кастомный аргумент 'parent_project'
        parent_project = kwargs.pop("parent_project", None)
        super().__init__(*args, **kwargs)

        # если есть родительский проект, фильтруем queryset
        if parent_project:
            responsible_filed = self.fields["responsible"]
            if not isinstance(responsible_filed, forms.ModelChoiceField):
                return

            responsible_filed.queryset = ProjectTeamMember.objects.filter(
                project=parent_project
            )


class TaskInlineForm(forms.ModelForm):
    """TaskInline admin model form."""

    class Meta:
        """Form metadata."""

        model = Task
        fields = "__all__"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Redefine main logic of form displaying."""
        # извлекаем кастомный аргумент 'parent_project'
        parent_project = kwargs.pop("parent_project", None)
        super().__init__(*args, **kwargs)

        # если есть родительский проект, фильтруем queryset
        if parent_project:
            assignee_filed = self.fields["assignee"]
            if not isinstance(assignee_filed, forms.ModelChoiceField):
                return

            assignee_filed.queryset = ProjectTeamMember.objects.filter(
                project=parent_project
            )
