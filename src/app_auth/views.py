"""Views for app_auth."""

from django.http import HttpRequest, JsonResponse


def healthcheck(request: HttpRequest) -> JsonResponse:
    """Check the project readiness."""
    return JsonResponse({"status": "ok"})
