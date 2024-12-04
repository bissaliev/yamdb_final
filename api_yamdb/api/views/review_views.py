from api.filters import TitleFilter
from api.mixins import CreateListDestroyViewSet
from api.permissions import ISAdminAuthorOrSuperuser, ISAdminOnlyEdit
from api.serializers.review_serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleReadSerializer,
    TitleSerializer,
)
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from reviews.models import Category, Genre, Review, Title

# TODO: Добавить использование select_related & prefetch_related


class TitleViewSet(viewsets.ModelViewSet):
    """Класс представления произведений."""

    queryset = Title.objects.all().annotate(rating_avg=Avg("reviews__score"))
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = [ISAdminOnlyEdit]

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TitleReadSerializer

        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Класс представления категорий произведений."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = [ISAdminOnlyEdit]


class GenreViewSet(CreateListDestroyViewSet):
    """Класс представления жанров произведений."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    lookup_field = "slug"
    permission_classes = [ISAdminOnlyEdit]


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ISAdminAuthorOrSuperuser]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ISAdminAuthorOrSuperuser]

    def get_queryset(self):
        pk = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review, pk=pk, title=self.kwargs.get("title_id")
        )
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get("title_id")
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(Review, title__id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)
