"""Django ORM models for app_auth."""

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from core.base_model import UUIDModel


class User(AbstractUser):
    """A main project User."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def __str__(self) -> str:
        """Model string representation."""
        return f"User {self.username}"


class Profile(UUIDModel):
    """User profile."""

    user = models.OneToOneField(
        to=User,
        null=False,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    phone = models.CharField(max_length=50, blank=True)

    def __str__(self) -> str:
        """String Model representation."""
        return f"User Profile {self.user.username}"

    class Meta:  # type: ignore
        """Additional Model metadata."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
