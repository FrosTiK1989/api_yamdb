from django_filters import rest_framework as rf_filters
from reviews.models import Title


class TitleFilter(rf_filters.FilterSet):
    category = rf_filters.CharFilter(field_name='category__slug')
    genre = rf_filters.CharFilter(field_name='genre__slug')
    name = rf_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )
    year = rf_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
