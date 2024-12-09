from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
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


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""

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

    def validate_username(self, value):
        if value == "me":
            raise serializers.ValidationError(
                "Вы не можете создать никнейм с данным значением."
            )

    def validate(self, data):
        current_user = self.context.get("request").user
        if data.get("role") and not current_user.is_admin:
            raise ValidationError("Вам нельзя менять свою роль.")

        return data
