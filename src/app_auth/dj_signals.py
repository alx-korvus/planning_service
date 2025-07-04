"""Django signals for app_auth."""

from typing import Any, Type

from django.db.models.signals import post_save
from django.dispatch import receiver

from app_auth.models import Profile, User


# receiver "подписывает" функцию на сигнал post_save от User
@receiver(signal=post_save, sender=User)
def create_user_profile(
    sender: Type[User],
    instance: User,
    created: bool,
    **kwargs: Any,
) -> None:
    """Creating a Profile after creating and saving a new User.

    This function will be executed every time after User.save() is called.

    Args:
        sender (Type[User]): User model class.
        instance (User): User class instance.
        created (bool): True if the object was created for the first time.
            False if the existing object was updated.
    """
    if created:
        Profile.objects.create(user=instance)
