"""Testing users."""

from typing import Any, Type, cast

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.management.base import BaseCommand
from faker import Faker

fake_instance = Faker()


class Command(BaseCommand):
    """Create fake users."""

    help = "Creates a fake users non-interactively."

    def handle(self, *args: Any, **options: Any) -> None:
        """Run it as management command."""
        User = cast(Type[AbstractUser], get_user_model())
        total_users: int = len(User.objects.all())
        if total_users > 1:
            self.stdout.write(
                self.style.SUCCESS(f"DB already has {total_users} users.")
            )
            return

        users_count: int = 10
        password = "12345678"

        for _ in range(users_count):
            User.objects.create_user(
                username=fake_instance.unique.user_name(),
                password=password,
                email=fake_instance.unique.email(),
                is_staff=True,
                is_active=True,
            )
        self.stdout.write(self.style.SUCCESS(f"Created {users_count} users."))
