from api.utils import generation_confirm_code, save_confirm_code_in_cache
from celery import shared_task
from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER

SENDER_EMAIL: str = EMAIL_HOST_USER


@shared_task
def send_confirm_code(recipient_email: str) -> None:
    """Задача генерирует код подтверждения и отправляет его на email."""
    confirm_code = generation_confirm_code()
    save_confirm_code_in_cache(recipient_email, confirm_code)
    subject = "Ваш код подтверждения"
    message = f"Ваш код подтверждения: {confirm_code}\n"
    send_mail(subject, message, SENDER_EMAIL, [recipient_email])
