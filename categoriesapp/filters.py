from django_filters import rest_framework as filters

from .models import Category


class CategoryFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    class Meta:
        model = Category
        fields = ['name']