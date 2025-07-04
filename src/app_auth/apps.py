"""Application settings for app_auth."""

from django.apps import AppConfig


class AppAuthConfig(AppConfig):
    """Main app config."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "app_auth"

    def ready(self) -> None:
        """Import signals when the app is ready."""
        import app_auth.dj_signals  # noqa
