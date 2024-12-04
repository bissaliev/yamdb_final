from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import USER, User


class RegisterAndSendConfirmCodeSerializer(serializers.ModelSerializer):
    """Сериализатор отправки кода на email."""

    confirmation_code = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        username = data["username"]
        if username == "me":
            raise ValidationError("Запрещённое имя пользователя.")
        return data

    class Meta:
        fields = ("email", "confirmation_code", "username")
        model = User


class CustomGetTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""

    # TODO: Проверка кода подтверждения
    confirmation_code = serializers.CharField()
    username = serializers.CharField()


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
