from django_filters.rest_framework import filters, FilterSet

from reviews.models import Title


class TitleFilter(FilterSet):
    """ Класс для фильтрации произведений. """
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    year = filters.NumberFilter(field_name="year")
    category = filters.CharFilter(
        field_name="category__slug", lookup_expr="icontains"
    )
    genre = filters.CharFilter(
        field_name="genre__slug", lookup_expr="icontains"
    )

    class Meta:
        model = Title
        fields = ("name", "year", "category", "genre",)
