from django_filters import FilterSet, filters
from reviews.models import Title


class CharFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class TitleFilter(FilterSet):
    genre = CharFilter(field_name='genre__slug', lookup_expr='in')
    category = CharFilter(field_name='category__slug', lookup_expr='in')

    class Meta:
        model = Title
        fields = ['year', 'name', 'genre', 'category']
