"""URL configuration for app_plan."""

from django.urls import include, path
from rest_framework import routers

from app_plan.views import ProjectViewSet

router = routers.DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="projects")

app_name = "app_plan"

urlpatterns = [
    path("", include(router.urls)),
]
