from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from users.models import User, USER
from reviews.models import Category, Genre, Title, Review, Comment


class RegisterAndSendConfirmCodeSerializer(serializers.ModelSerializer):
    """ Сериализатор отправки кода на email. """
    confirmation_code = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        username = data["username"]
        if username == "me":
            raise ValidationError("Запрещённое имя пользователя.")
        return data

    class Meta:
        fields = ("email", "confirmation_code", "username")
        model = User


class CategorySerializer(serializers.ModelSerializer):
    """ Сериализатор для получения и создания категорий произведений. """

    class Meta:
        fields = ("name", "slug",)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """ Сериализатор для получения и создания жанров произведений. """

    class Meta:
        fields = ("name", "slug",)
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания и редактирования произведений. """
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = ("id", "name", "year", "description", "category", "genre",)
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """ Сериализатор для получения произведений. """
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(
        source="reviews__score__avg", read_only=True
    )

    class Meta:
        fields = "__all__"
        model = Title


class CustomGetTokenSerializer(serializers.Serializer):
    """ Сериализатор получения токена. """

    confirmation_code = serializers.CharField()
    username = serializers.CharField()


class GetOrCreateUsersSerializer(serializers.ModelSerializer):
    """ Создаём или получаем пользователей. """

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


class GetInfoAboutMeSerializer(serializers.ModelSerializer):
    """ Сериализатор получения информации о пользователе. """

    def validate(self, data):

        if (
            self.context.get("request").user.role == USER
            and data.get("role")
        ):
            raise ValidationError("Вам нельзя менять свою роль.")

        return data

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


class CertainUserSerializer(serializers.ModelSerializer):
    """ Сериализатор для конкретного пользователя. """

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


class ReviewSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания и редактирования отзывов. """
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    title = serializers.SlugRelatedField(
        read_only=True, slug_field="id")

    class Meta:
        model = Review
        fields = "__all__"

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        score = data["score"]

        if request.method != "POST":
            return data
        if Review.objects.filter(
            title=get_object_or_404(Title, pk=title_id),
            author=request.user
        ).exists():
            raise ValidationError(
                "Вы можете оставить только "
                "один отзыв на произведение"
            )
        if 0 > score > 10:
            raise ValidationError("Оценка")

        return data


class CommentSerializer(serializers.ModelSerializer):
    """ Сериализатор для создания и редактирования комментариев на отзыв. """
    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "review", "pub_date")
