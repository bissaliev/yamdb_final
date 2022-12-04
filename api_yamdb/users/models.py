from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

ADMIN = "admin"
MODERATOR = "moderator"
USER = "user"
USER_ROLES = (
    (ADMIN, "Administrator"),
    (MODERATOR, "Moderator"),
    (USER, "User"),
)


class User(AbstractUser):
    """ Переопределяем поля пользователя. """

    email = models.EmailField(_("email address"), unique=True)
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    password = models.CharField(max_length=100, blank=True, null=True)
    role = models.CharField(
        "Роль", max_length=30,
        choices=USER_ROLES, default="user"
    )
    confirmation_code = models.CharField(max_length=100)

    @property
    def is_admin(self):
        return (
            ADMIN in self.role
            or self.is_staff
            or self.is_superuser
        )

    @property
    def is_moderator(self):
        return MODERATOR in self.role

    @property
    def is_user(self):
        return USER in self.role
