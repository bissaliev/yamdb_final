import random

from django.conf import settings
from django.core.cache import cache

CACHE_KEY: str = settings.CACHE_KEY_CONFIRM_CODE
CACHE_TIMEOUT: int = settings.CACHE_TIMEOUT


def generation_confirm_code() -> str:
    """Генерация 6 значного кода верификации."""
    return str(random.randint(111111, 999999))


def save_confirm_code_in_cache(email: str, confirm_code: str) -> None:
    """Сохранение кода подтверждения в кеше."""
    cache.set(f"{CACHE_KEY}_{email}", confirm_code, timeout=CACHE_TIMEOUT)


def get_confirm_code_from_cache(email: str) -> str:
    """Получение кода подтверждения из кеша."""
    confirm_code = cache.get(f"{CACHE_KEY}_{email}")
    return confirm_code


def verify_confirm_code(email: str, confirm_code: str) -> bool:
    """
    Верификация кода подтверждения из кеша с кодом предоставленным
    пользователем.
    """
    cache_confirm_code = get_confirm_code_from_cache(email)
    return cache_confirm_code == confirm_code
