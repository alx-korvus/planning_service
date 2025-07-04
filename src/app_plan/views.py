"""API endpoints in the app_plan."""

from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ModelSerializer

from app_plan.models import Project
from app_plan.serializers import ProjectDetailSerializer, ProjectListSerializer


class ProjectViewSet(ModelViewSet):
    """DRF ViewSet for a Project model."""

    queryset = (
        Project.objects.all().order_by("created_at").select_related("manager")
    )

    def get_serializer_class(self) -> type[ModelSerializer]:
        """Return different serializers for list and detail actions."""
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer
