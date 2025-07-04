"""Custom formsets for app_plan."""

from django.forms.models import BaseInlineFormSet


class StageInlineFormSet(BaseInlineFormSet):
    """Custom formset for StageInline admin model."""

    def get_form_kwargs(self, index: int | None) -> dict:
        """Add parent Project to kwargs for a form."""
        kwargs = super().get_form_kwargs(index)
        kwargs["parent_project"] = self.instance
        return kwargs
