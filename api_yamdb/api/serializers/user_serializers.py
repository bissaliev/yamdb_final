from api.tasks import send_confirm_code
from api.utils import verify_confirm_code
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class SendConfirmCodeSerializer(serializers.Serializer):
    """Отправка кода верификации на email пользователя."""

    email = serializers.EmailField(required=True)

    def save(self):
        """Генерация код верификации и отправка пользователю на email."""
        email = self.validated_data["email"]
        send_confirm_code.delay(email)


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
        if not verify_confirm_code(email, confirm_code):
            raise serializers.ValidationError(
                "Неверный код верификации или код просрочен."
            )
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
        """Роль пользователя может изменить только администратор."""
        current_user = self.context.get("request").user
        if data.get("role") and not current_user.is_admin:
            raise ValidationError(
                "Роль пользователя может изменить только администратор."
            )

        return data
