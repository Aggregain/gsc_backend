import django_filters
from django.db.models import Q

from common.models import Program


class ProgramFilter(django_filters.FilterSet):
    specialty_group = django_filters.BaseInFilter(field_name='specialities__specialty_group__name', lookup_expr='in', label='группы специальностей')
    name = django_filters.BaseInFilter(field_name='name', lookup_expr='in', label='название программы')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='минимальная стоимость')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='максимальная стоимость')
    language = django_filters.BaseInFilter(field_name='language', lookup_expr='in', label='язык обучения')
    study_format = django_filters.BaseInFilter(field_name='format', lookup_expr='in', label='формат обучения')
    admission_deadline_after = django_filters.DateFilter(
        field_name='admission_deadline',
        lookup_expr='gte',
        label='Дедлайн после или в эту дату'
    )

    admission_deadline_before = django_filters.DateFilter(
        field_name='admission_deadline',
        lookup_expr='lte',
        label='Дедлайн до или в эту дату'
    )
    city = django_filters.BaseInFilter(
        field_name='education_place__city__name',
        lookup_expr='in',
        label='Город (название)'
    )
    country = django_filters.BaseInFilter(
        field_name='education_place__city__country__name',
        lookup_expr='in',
        label='Страна (название)'
    )
    requirement_names = django_filters.BaseInFilter(
        field_name='academic_requirements__name',
        lookup_expr='in',
        label='Названия требований (список)'
    )

    requirements = django_filters.CharFilter(
        method='filter_multiple_requirements',
        label='Требования (название:порог через запятую)'
    )



    def filter_multiple_requirements(self, queryset, name, value):
        requirements = value.split(',')
        q_objects = Q()
        for req in requirements:
            if ':' in req:
                req_name, req_treshold = req.split(':')
                q_objects |= Q(
                    academic_requirements__name__iexact=req_name.strip(),
                    academic_requirements__treshold__lte=float(req_treshold)
                )
        return queryset.filter(q_objects).distinct()

    class Meta:
        model = Program
        fields = ['language',
                  'study_format',
                  'city',
                  'country',
                  'name',
                  'price_min',
                  'price_max',
                  'admission_deadline_after',
                  'admission_deadline_before',
                  'requirements'
                  ]




