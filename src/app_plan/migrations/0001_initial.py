"""Initial migration for app_plan."""

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    """Django Migration."""

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Artifact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "title",
                    models.CharField(
                        max_length=255, verbose_name="Artifact name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="artifacts/%Y/%m/%d/", verbose_name="File"
                    ),
                ),
                ("object_id", models.UUIDField()),
                (
                    "content_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.contenttype",
                    ),
                ),
            ],
            options={
                "verbose_name": "Artifact",
                "verbose_name_plural": "Artifacts",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Project name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                ("date_start", models.DateField(verbose_name="Start date")),
                ("date_end", models.DateField(verbose_name="End date")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Not started"),
                            ("progress", "In progress"),
                            ("done", "Done"),
                            ("archived", "Archived"),
                        ],
                        default="new",
                        max_length=10,
                        verbose_name="Execution status",
                    ),
                ),
                (
                    "manager",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="managed_projects",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Project manager",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "full_name",
                    models.CharField(max_length=255, verbose_name="Full name"),
                ),
                (
                    "role",
                    models.CharField(
                        max_length=150, verbose_name="Role/position"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="Email"
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        blank=True, max_length=50, verbose_name="Phone number"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="contacts",
                        to="app_plan.project",
                        verbose_name="Project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Contact",
                "verbose_name_plural": "Contacts",
            },
        ),
        migrations.CreateModel(
            name="ProjectTeamMember",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "role",
                    models.CharField(
                        max_length=100, verbose_name="Role in the project"
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app_plan.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Team member",
                "verbose_name_plural": "Team members",
                "unique_together": {("project", "user")},
            },
        ),
        migrations.AddField(
            model_name="project",
            name="team",
            field=models.ManyToManyField(
                related_name="projects_in",
                through="app_plan.ProjectTeamMember",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Project team",
            ),
        ),
        migrations.CreateModel(
            name="Stage",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(
                        max_length=255, verbose_name="Stage name"
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                ("date_start", models.DateField(verbose_name="Start date")),
                ("date_end", models.DateField(verbose_name="End date")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Not started"),
                            ("progress", "In progress"),
                            ("done", "Done"),
                            ("archived", "Archived"),
                        ],
                        default="new",
                        max_length=10,
                        verbose_name="Execution status",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stages",
                        to="app_plan.project",
                        verbose_name="Project",
                    ),
                ),
                (
                    "responsible",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="responsible_for_stage",
                        to="app_plan.projectteammember",
                        verbose_name="Responsible for the stage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project stage",
                "verbose_name_plural": "Project stages",
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "name",
                    models.CharField(max_length=255, verbose_name="Task name"),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, null=True, verbose_name="Description"
                    ),
                ),
                ("date_start", models.DateField(verbose_name="Start date")),
                ("date_end", models.DateField(verbose_name="End date")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("new", "Not started"),
                            ("progress", "In progress"),
                            ("done", "Done"),
                            ("archived", "Archived"),
                        ],
                        default="new",
                        max_length=10,
                        verbose_name="Execution status",
                    ),
                ),
                (
                    "assignee",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_tasks",
                        to="app_plan.projectteammember",
                        verbose_name="Task assignee",
                    ),
                ),
                (
                    "stage",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tasks",
                        to="app_plan.stage",
                        verbose_name="Stage",
                    ),
                ),
            ],
            options={
                "verbose_name": "Task",
                "verbose_name_plural": "Tasks",
            },
        ),
    ]
