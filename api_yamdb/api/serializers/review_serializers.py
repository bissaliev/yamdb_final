from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения и создания категорий произведений."""

    class Meta:
        model = Category
        fields = (
            "name",
            "slug",
        )


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и создания жанров произведений."""

    class Meta:
        model = Genre
        fields = (
            "name",
            "slug",
        )


class TitleBaseSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )


class TitleCreateSerializer(TitleBaseSerializer):
    """Сериализатор для создания и редактирования произведений."""

    pass


class TitleReadSerializer(TitleBaseSerializer):
    """Сериализатор для получения произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(source="rating_avg", read_only=True)

    class Meta(TitleBaseSerializer.Meta):
        model = Title
        fields = TitleBaseSerializer.Meta.fields + ("rating",)


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

        extra_kwargs = {
            "score": {
                "error_messages": {
                    "min_value": "Минимальное значение должно быть 1.",
                    "max_value": "Максимальное значение должно быть 10.",
                    "invalid": "Введите корректное целое число.",
                }
            },
            "text": {
                "error_messages": {"blank": "Это поле не может быть пустым."}
            },
        }

    def validate(self, data):
        request = self.context["request"]
        title_id = self.context["view"].kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)

        if request.method != "POST":
            return data
        if Review.objects.filter(title=title, author=request.user).exists():
            raise ValidationError(
                "Вы можете оставить только один отзыв на произведение"
            )
        data["title"] = title

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования комментариев на отзыв."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ("id", "review", "pub_date")
