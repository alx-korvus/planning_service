"""Django ORM models for app_plan."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from app_auth.models import User
from core.base_model import UUIDModel


class StatusChoices(models.TextChoices):
    """Progress statuses for projects, stages and tasks."""

    NOT_STARTED = "new", "Not started"
    IN_PROGRESS = "progress", "In progress"
    COMPLETED = "done", "Done"
    ARCHIVED = "archived", "Archived"


class Project(UUIDModel):
    """Project Model."""

    name = models.CharField(verbose_name="Project name", max_length=255)
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    date_start = models.DateField(verbose_name="Start date")
    date_end = models.DateField(verbose_name="End date")
    manager = models.ForeignKey(
        to=User,
        verbose_name="Project manager",
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_projects",
    )
    team: models.ManyToManyField = models.ManyToManyField(
        to=User,
        verbose_name="Project team",
        through="ProjectTeamMember",
        related_name="projects_in",
    )
    status = models.CharField(
        verbose_name="Execution status",
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.NOT_STARTED,
    )

    stages: models.Manager["Stage"]

    @property
    def completion_percentage(self) -> int:
        """Calculate the percentage of project completion.

        Based on completed stages.
        """
        stages = self.stages.all()
        if not stages.exists():
            return 0
        completed = stages.filter(status=StatusChoices.COMPLETED).count()
        return round((completed / stages.count()) * 100)

    def __str__(self) -> str:
        """Model string representation."""
        return self.name

    class Meta:  # type:ignore
        """Model metadata."""

        verbose_name = "Project"
        verbose_name_plural = "Projects"


class ProjectTeamMember(UUIDModel):
    """Secondary model for linking a Project and a User.

    Uses an indication of the role.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(verbose_name="Role in the project", max_length=100)

    def __str__(self) -> str:
        """Model string representation."""
        return f"Teammate {self.user.username}"

    class Meta:  # type:ignore
        """Model metadata."""

        verbose_name = "Team member"
        verbose_name_plural = "Team members"
        # Один пользователь - одна роль в проекте:
        unique_together = ("project", "user")


class Stage(UUIDModel):
    """Project stage model."""

    project = models.ForeignKey(
        to=Project,
        verbose_name="Project",
        on_delete=models.CASCADE,
        related_name="stages",
    )
    name = models.CharField(verbose_name="Stage name", max_length=255)
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    date_start = models.DateField(verbose_name="Start date")
    date_end = models.DateField(verbose_name="End date")

    responsible = models.ForeignKey(
        to=ProjectTeamMember,
        verbose_name="Responsible for the stage",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="responsible_for_stage",
    )

    status = models.CharField(
        verbose_name="Execution status",
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.NOT_STARTED,
    )

    tasks: models.Manager["Task"]

    @property
    def completion_percentage(self) -> float:
        """Calculate the percentage of stage completion.

        Based on completed tasks.
        """
        tasks = self.tasks.all()
        if not tasks.exists():
            return 0
        completed_tasks = tasks.filter(status=StatusChoices.COMPLETED).count()
        return round((completed_tasks / tasks.count()) * 100)

    def __str__(self) -> str:
        """Model string representation."""
        base_str: str = f"Stage {self.name} in project {self.project.name}"
        if not self.responsible:
            return base_str

        resp_name: str = f"; responsible {self.responsible.user.username}"
        return base_str + resp_name

    class Meta:  # type:ignore
        """Model metadata."""

        verbose_name = "Project stage"
        verbose_name_plural = "Project stages"


class Task(UUIDModel):
    """Task model."""

    stage = models.ForeignKey(
        to=Stage,
        verbose_name="Stage",
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    name = models.CharField("Task name", max_length=255)
    description = models.TextField("Description", blank=True, null=True)
    date_start = models.DateField("Start date")
    date_end = models.DateField("End date")

    assignee = models.ForeignKey(
        to=ProjectTeamMember,
        verbose_name="Task assignee",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_tasks",
    )

    status = models.CharField(
        verbose_name="Execution status",
        max_length=10,
        choices=StatusChoices.choices,
        default=StatusChoices.NOT_STARTED,
    )

    def __str__(self) -> str:
        """Model string representation."""
        base_str: str = f"Task {self.name} in stage {self.stage.name}"
        if not self.assignee:
            return base_str

        resp_name: str = f"; assignee {self.assignee.user.username}"
        return base_str + resp_name

    class Meta:  # type:ignore
        """Model metadata."""

        verbose_name = "Task"
        verbose_name_plural = "Tasks"


class Artifact(UUIDModel):
    """Model for storing artifacts (documents, files).

    Use GenericForeignKey to connect with any model (Project, Stage, Task).
    """

    title = models.CharField(verbose_name="Artifact name", max_length=255)
    description = models.TextField(
        verbose_name="Description",
        blank=True,
        null=True,
    )
    file = models.FileField(
        verbose_name="File",
        upload_to="artifacts/%Y/%m/%d/",
    )

    # Generic relation
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey(
        ct_field="content_type",
        fk_field="object_id",
    )

    def __str__(self) -> str:
        """Model string representation."""
        return self.title

    class Meta:  # type:ignore
        """Model metadata."""

        verbose_name = "Artifact"
        verbose_name_plural = "Artifacts"


class Contact(UUIDModel):
    """Contact details and persons not performing the project."""

    project = models.ForeignKey(
        to=Project,
        verbose_name="Project",
        on_delete=models.CASCADE,
        related_name="contacts",
    )
    full_name = models.CharField(verbose_name="Full name", max_length=255)
    role = models.CharField(verbose_name="Role/position", max_length=150)
    email = models.EmailField(verbose_name="Email", blank=True)
    phone = models.CharField(
        verbose_name="Phone number",
        max_length=50,
        blank=True,
    )

    def __str__(self) -> str:
        """Model string representation."""
        return f"Contact {self.full_name}"

    class Meta:  # type:ignore
        """Model metadata."""

        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
