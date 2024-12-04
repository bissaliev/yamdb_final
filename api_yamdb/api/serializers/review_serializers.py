from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для получения и создания категорий произведений."""

    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для получения и создания жанров произведений."""

    class Meta:
        fields = (
            "name",
            "slug",
        )
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования произведений."""

    category = serializers.SlugRelatedField(
        slug_field="slug", queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field="slug", many=True, queryset=Genre.objects.all()
    )

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "description",
            "category",
            "genre",
        )
        model = Title


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для получения произведений."""

    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(source="rating_avg", read_only=True)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category",
        )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для создания и редактирования отзывов."""

    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )
    title = serializers.SlugRelatedField(read_only=True, slug_field="id")

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
            title=get_object_or_404(Title, pk=title_id), author=request.user
        ).exists():
            raise ValidationError(
                "Вы можете оставить только " "один отзыв на произведение"
            )
        if 0 > score > 10:
            raise ValidationError("Оценка")

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
