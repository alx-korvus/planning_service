"""Base project model."""

import uuid

from django.db import models


class UUIDModel(models.Model):
    """Abstract base model class."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        """Additional Model metadata."""

        abstract = True
