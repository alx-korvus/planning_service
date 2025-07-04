"""Admin panel settings for app_auth."""

from typing import Any

from django.contrib import admin
from django.contrib.admin.options import InlineModelAdmin
from django.contrib.auth.admin import UserAdmin
from django.http.request import HttpRequest

from app_auth.models import Profile, User


class ProfileInline(admin.StackedInline):
    """Inline Profile representation."""

    model = Profile
    can_delete = False  # запретить удаление профиля через админку
    verbose_name = "Profile"
    verbose_name_plural = "Profiles"
    fk_name = "user"


class CustomUserAdmin(UserAdmin):
    """Overridden User Admin model."""

    inlines = (ProfileInline,)

    def get_inline_instances(
        self,
        request: HttpRequest,
        obj: Any | None = None,
    ) -> list[InlineModelAdmin]:
        """Prevents inlines from showing on the 'add' page."""
        if not obj:
            return list()

        return super().get_inline_instances(request, obj)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile Admin model."""

    readonly_fields = ("id", "created_at", "updated_at", "user")
    list_display = ("user", "get_user_email", "phone")
    search_fields = ("user__username", "user__email", "phone")

    # отображение в форме редактирования
    fieldsets = (
        ("Main info", {"fields": ("user", "phone")}),
        (
            "Service info",
            {
                "fields": ("id", "created_at", "updated_at", "is_active"),
                "classes": ("collapse",),  # скрыть блок по умолчанию
            },
        ),
    )

    @admin.display(description="User email", ordering="user__email")
    def get_user_email(self, obj: Profile) -> str:
        """Return related User email."""
        return obj.user.email

    def has_add_permission(self, request: HttpRequest) -> bool:
        """Disable the ability to add new profiles manually."""
        return False


if admin.site.is_registered(User):
    # отменяем регистрацию стандартной модели User
    admin.site.unregister(User)

admin.site.register(User, CustomUserAdmin)
