"""Initialize superuser."""

import os
from typing import Any, Type, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create superuser."""

    help = "Creates a superuser non-interactively if it does not exist."

    def handle(self, *args: Any, **options: Any) -> None:
        """Run it as management command."""
        User = cast(Type[AbstractUser], get_user_model())

        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "admin")

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser {username} already exists.")
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser {username} created."))
