"""Admin panel settings for app_plan."""

from typing import Any, Generic, Type, TypeVar

from django import forms
from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db import models
from django.forms import Textarea
from django.http.request import HttpRequest

from app_plan.forms import StageInlineForm, TaskInlineForm
from app_plan.formsets import StageInlineFormSet, TaskInlineFormSet
from app_plan.models import (
    Artifact,
    Contact,
    Project,
    ProjectTeamMember,
    Stage,
    Task,
)

ModelType = TypeVar("ModelType", bound=models.Model)

custom_formfield_overrides: dict[Type[models.Field], dict[str, Any]] = {
    models.TextField: {"widget": Textarea(attrs={"rows": 2, "cols": 32})},
}


class CommonModelAdmin(admin.ModelAdmin, Generic[ModelType]):
    """Implementation of common behavior of admin models."""

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: ModelType | None = None,
    ) -> list[str]:
        """Get read-only fields for existing objects only."""
        # если это страница редактирования, а не создания
        if obj:
            return ["id", "created_at", "updated_at"]
        # на странице создания убираем поля "только для чтения"
        return []

    def get_exclude(
        self,
        request: HttpRequest,
        obj: ModelType | None = None,
    ) -> list[str]:
        """Hide certain fields on the add page."""
        # получаем стандартный список исключений
        excluded = super().get_exclude(request, obj) or []
        if isinstance(excluded, tuple):
            excluded = list(excluded)

        # если это страница создания нового объекта (obj is None)
        if not obj:
            # добавляем поля, которые нужно скрыть при создании
            excluded.extend(["id", "created_at", "updated_at", "is_active"])

        return excluded


class ArtifactInline(GenericTabularInline):
    """Inline Artifact representation."""

    model = Artifact
    extra = 1  # кол-во пустых форм для добавления
    formfield_overrides = custom_formfield_overrides


class ProjectTeamMemberInline(admin.TabularInline):
    """Inline Project Team management."""

    model = ProjectTeamMember
    extra = 1
    verbose_name = "Teammate"
    verbose_name_plural = "Project Team"


class ContactInline(admin.TabularInline):
    """Inline Project Contacts management."""

    model = Contact
    extra = 1


class StageInline(admin.TabularInline):
    """Inline Stages representation. Use as inner block for a Projects."""

    model = Stage
    form = StageInlineForm
    formset = StageInlineFormSet
    extra = 1  # кол-во пустых строк для заполнения
    show_change_link = True  # ссылка на страницу редактирования этапа
    fields = ("name", "responsible", "date_start", "date_end", "status")
    readonly_fields = ("completion_percentage",)


class TaskInline(admin.TabularInline):
    """Inline Task representation."""

    model = Task
    form = TaskInlineForm
    formset = TaskInlineFormSet
    extra = 1
    fields = ("name", "assignee", "date_start", "date_end", "status")


@admin.register(Project)
class ProjectAdmin(CommonModelAdmin):
    """Project Admin model."""

    list_display = (
        "name",
        "manager",
        "status",
        "date_start",
        "date_end",
        "completion_percentage",
    )
    list_filter = ("status", "manager")
    search_fields = ("name", "description")
    formfield_overrides = custom_formfield_overrides

    # встраиваем управление командой, этапами, контактами и артефактами
    inlines = (
        ProjectTeamMemberInline,
        StageInline,
        ContactInline,
        ArtifactInline,
    )

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Project | None = None,
    ) -> list[str]:
        """Extend the base read-only fields with Project-specific ones."""
        readonly_fields = super().get_readonly_fields(request, obj)

        if obj:
            readonly_fields.insert(0, "completion_percentage")

        return readonly_fields

    def get_exclude(
        self,
        request: HttpRequest,
        obj: Project | None = None,
    ) -> list[str]:
        """Extend the base excluded fields with Project-specific ones."""
        excluded = super().get_exclude(request, obj)

        if obj:
            excluded.append("completion_percentage")

        return excluded

    def get_inline_instances(
        self,
        request: HttpRequest,
        obj: Any | None = None,
    ) -> list[InlineModelAdmin]:
        """Conditionally displays inlines on the 'add' page."""
        if obj:
            return super().get_inline_instances(request, obj)

        # на странице создания не отображаем StageInline
        inlines: list[InlineModelAdmin] = []
        for inline_cls in self.inlines:
            if inline_cls != StageInline:
                inlines.append(inline_cls(self.model, self.admin_site))
        return inlines


@admin.register(Stage)
class StageAdmin(CommonModelAdmin):
    """Stage Admin model."""

    list_display = (
        "name",
        "project",
        "responsible",
        "status",
        "date_start",
        "date_end",
        "completion_percentage",
    )
    list_filter = ("status", "project", "responsible")
    search_fields = ("name",)
    formfield_overrides = custom_formfield_overrides

    # встраиваем управление задачами и артефактами
    inlines = (TaskInline, ArtifactInline)

    def get_inline_instances(
        self,
        request: HttpRequest,
        obj: Any | None = None,
    ) -> list[InlineModelAdmin]:
        """Conditionally displays inlines on the 'add' page."""
        if obj:
            return super().get_inline_instances(request, obj)

        # на странице создания не отображаем TaskInline
        inlines: list[InlineModelAdmin] = []
        for inline_cls in self.inlines:
            if inline_cls != TaskInline:
                inlines.append(inline_cls(self.model, self.admin_site))
        return inlines

    def formfield_for_foreignkey(
        self,
        db_field: models.ForeignKey,
        request: HttpRequest,
        **kwargs: Any,
    ) -> forms.ModelChoiceField | None:
        """Filter list of Project Team members.

        Show only the current project's participants.
        """
        if db_field.name == "responsible":
            # Пытаемся получить ID объекта из URL, чтобы найти проект
            # Это сработает на странице редактирования существующего этапа
            if not request.resolver_match:
                return super().formfield_for_foreignkey(
                    db_field,
                    request,
                    **kwargs,
                )

            stage_id = request.resolver_match.kwargs.get("object_id")
            if stage_id:
                try:
                    stage = Stage.objects.get(pk=stage_id)
                    # фильтр по проекту, к которому относится этап
                    kwargs["queryset"] = ProjectTeamMember.objects.filter(
                        project=stage.project,
                    )
                except Stage.DoesNotExist:
                    pass

        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(
        self,
        request: HttpRequest,
        obj: Stage | None = None,
    ) -> list[str]:
        """Extend the base read-only fields with Project-specific ones."""
        readonly_fields = super().get_readonly_fields(request, obj)

        if obj:
            readonly_fields.insert(0, "completion_percentage")

        return readonly_fields

    def get_exclude(
        self,
        request: HttpRequest,
        obj: Stage | None = None,
    ) -> list[str]:
        """Extend the base excluded fields with Project-specific ones."""
        excluded = super().get_exclude(request, obj)

        if obj:
            excluded.append("completion_percentage")

        return excluded


@admin.register(Task)
class TaskAdmin(CommonModelAdmin):
    """Task Admin model."""

    list_display = (
        "name",
        "stage",
        "assignee",
        "status",
        "date_start",
        "date_end",
    )
    list_filter = (
        "status",
        "assignee",
    )
    search_fields = ("name",)
    formfield_overrides = custom_formfield_overrides

    # встраиваем управление артефактами
    inlines = (ArtifactInline,)

    def formfield_for_foreignkey(
        self,
        db_field: models.ForeignKey,
        request: HttpRequest,
        **kwargs: Any,
    ) -> forms.ModelChoiceField | None:
        """Filter list of Project Team members.

        Show only the current project's participants.
        """
        if db_field.name == "assignee":
            if not request.resolver_match:
                return super().formfield_for_foreignkey(
                    db_field,
                    request,
                    **kwargs,
                )

            task_id = request.resolver_match.kwargs.get("object_id")
            if task_id:
                try:
                    task = Task.objects.get(pk=task_id)
                    # фильтр по проекту, к которому относится этап задачи
                    kwargs["queryset"] = ProjectTeamMember.objects.filter(
                        project=task.stage.project,
                    )
                except Task.DoesNotExist:
                    pass

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Artifact)
class ArtifactAdmin(CommonModelAdmin):
    """Artifact Admin model."""

    ...


@admin.register(Contact)
class ContactAdmin(CommonModelAdmin):
    """Contact Admin model."""

    ...
