import django_filters

from applications.models import Application


class ApplicationFilter(django_filters.FilterSet):
    countries = django_filters.BaseInFilter(
        field_name='program__education_place__city__country__id',
        lookup_expr='in',
        label='Страна (id)'
    )
    cities = django_filters.BaseInFilter(
        field_name='program__education_place__city__id',
        lookup_expr='in',
        label='Город (id)'
    )
    education_places = django_filters.BaseInFilter(
        field_name='program__education_place__id',
    )

    class Meta:
        model = Application
        fields = [
            'countries',
            'cities',
           'education_places'
        ]