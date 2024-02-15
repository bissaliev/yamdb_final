import os
from dotenv import load_dotenv
from typing import Any
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.shortcuts import get_object_or_404

load_dotenv()

User = get_user_model()


class Command(BaseCommand):
    help = "Create superuser"

    def handle(self, *args: Any, **options: Any):
        call_command(
            "createsuperuser",
            f'--username={os.getenv("DJANGO_SUPERUSER_USERNAME")}',
            f'--email={os.getenv("DJANGO_SUPERUSER_EMAIL")}',
            interactive=False,
        )
        user = get_object_or_404(User, username="admin")
        if user:
            user.set_password(os.getenv("DJANGO_SUPERUSER_PASSWORD"))
            user.save()
            self.stdout.write(self.style.SUCCESS("Суперпользователь создан."))
        else:
            self.stdout.write(self.style.ERROR("Суперпользователь не создан."))
