import random

from django.core.mail import send_mail

from api_yamdb.settings import EMAIL_HOST_USER

SENDER_EMAIL = EMAIL_HOST_USER


def generation_confirm_code() -> str:
    """Генерация 6 значного кода верификации."""
    return str(random.randint(111111, 999999))


def send_conf_code(recipient_email: str, confirmation_code: str) -> None:
    """Отправка кода верификации пользователю на email."""
    subject = "Ваш код подтверждения"
    message = f"Ваш код подтверждения: {confirmation_code}\n"
    send_mail(subject, message, SENDER_EMAIL, [recipient_email])
