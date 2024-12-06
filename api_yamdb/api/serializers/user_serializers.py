from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import USER
from users.utils import generation_confirm_code, send_conf_code

User = get_user_model()

CACHE_KEY = settings.CACHE_KEY_CONFIRM_CODE
CACHE_TIMEOUT = settings.CACHE_TIMEOUT


class SendConfirmCodeSerializer(serializers.Serializer):
    """Отправка кода верификации на email пользователя."""

    email = serializers.EmailField(required=True)

    def save(self):
        """Генерация код верификации и отправка пользователю на email."""
        confirm_code = generation_confirm_code()
        email = self.validated_data["email"]
        send_conf_code(email, confirm_code)
        cache.set(f"{CACHE_KEY}_{email}", confirm_code, timeout=CACHE_TIMEOUT)


class CustomGetTokenSerializer(serializers.Serializer):
    """
    Верификация кода подтверждения, отправленный на email пользователя,
    со значением, сохранённым в кеше.
    """

    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(
        required=True, min_length=6, max_length=6, label="Код верификации"
    )

    def validate(self, attrs):
        """Верифицируем код подтверждения."""
        confirm_code = attrs.get("confirmation_code")
        email = attrs.get("email")
        cache_confirm_code = cache.get(f"{CACHE_KEY}_{email}")
        if cache_confirm_code is None or confirm_code != cache_confirm_code:
            raise serializers.ValidationError(
                "Неверный код верификации или код просрочен."
            )
        cache.delete(f"{CACHE_KEY}_{email}")
        return attrs

    def save(self):
        """Получаем или сохраняем пользователя и возвращаем его."""
        email = self.validated_data["email"]
        user, _ = User.objects.get_or_create(email=email)
        return user


class BaseUserSerializer(serializers.ModelSerializer):
    """Базовый класс сериализатор пользователя."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )
        extra_kwargs = {"role": {"read_only": True}}


class GetOrCreateUsersSerializer(BaseUserSerializer):
    """Создаём или получаем пользователей."""

    pass


class GetInfoAboutMeSerializer(BaseUserSerializer):
    """Сериализатор получения информации о пользователе."""

    # TODO: Возможно переместить проверку в пермишены
    def validate(self, data):
        if self.context.get("request").user.role == USER and data.get("role"):
            raise ValidationError("Вам нельзя менять свою роль.")

        return data


class CertainUserSerializer(BaseUserSerializer):
    """Сериализатор для конкретного пользователя."""

    pass
