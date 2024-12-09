from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    """Модель пользователя."""

    class Role(models.TextChoices):
        ADMIN = "admin"
        MODERATOR = "moderator"
        USER = "user"

    email = models.EmailField(_("email address"), unique=True, db_index=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Пользователь",
    )
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.CharField(
        "Роль", max_length=30, choices=Role, default=Role.USER
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    @property
    def is_admin(self):
        return (
            self.Role.ADMIN.value in self.role
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.Role.MODERATOR.value in self.role

    @property
    def is_user(self):
        return self.Role.USER.value in self.role

    def get_token(self) -> dict[str, str]:
        refresh = RefreshToken.for_user(self)
        return {"token": str(refresh.access_token)}
