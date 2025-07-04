"""DRF serializers for app_plan."""

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    StringRelatedField,
)

from app_plan.models import Project


class ProjectListSerializer(ModelSerializer):
    """Serializer for the list of projects."""

    manager = StringRelatedField(read_only=True)  # type: ignore
    detail_url = HyperlinkedIdentityField(
        view_name="app_plan:projects-detail",
        lookup_field="pk",
    )

    class Meta:  # type: ignore
        """Serializer metadata."""

        model = Project
        fields = (
            "id",
            "name",
            "date_start",
            "date_end",
            "manager",
            "status",
            "completion_percentage",
            "detail_url",
        )


class ProjectDetailSerializer(ModelSerializer):
    """Serializer for the project details."""

    manager = StringRelatedField(read_only=True)  # type: ignore

    class Meta:  # type: ignore
        """Serializer metadata."""

        model = Project
        fields = "__all__"
