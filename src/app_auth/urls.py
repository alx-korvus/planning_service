"""URL configuration for app_auth."""

from django.urls import path

from app_auth.views import healthcheck

app_name = "app_auth"

urlpatterns = [
    path("healthcheck/", healthcheck, name="healthcheck"),
]
