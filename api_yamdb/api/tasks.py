import random

from celery import shared_task
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER

SENDER_EMAIL = EMAIL_HOST_USER


def generation_confirm_code() -> str:
    """Генерация 6 значного кода верификации."""
    return str(random.randint(111111, 999999))


@shared_task
def send_confirm_code(email: str, confirm_code: str):
    # confirm_code = generation_confirm_code()
    subject = "Ваш код подтверждения"
    message = f"Ваш код подтверждения: {confirm_code}\n"
    send_mail(subject, message, SENDER_EMAIL, [email])
