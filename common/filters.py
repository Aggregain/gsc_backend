import django_filters

from common.models import Program


class ProgramFilter(django_filters.FilterSet):
    countries = django_filters.BaseInFilter(
        field_name='education_place__city__country__id',
        lookup_expr='in',
        label='Страна (название)'
    )
    cities = django_filters.BaseInFilter(
        field_name='education_place__city__id',
        lookup_expr='in',
        label='Город (название)'
    )
    names = django_filters.BaseInFilter(field_name='name', lookup_expr='in', label='название программы')
    specialty_groups = django_filters.BaseInFilter(field_name='specialities__specialty_group__id', lookup_expr='in',
                                                   label='группы специальностей')
    languages = django_filters.BaseInFilter(field_name='language', lookup_expr='in', label='язык обучения')
    admission_deadline_before = django_filters.DateFilter(
        field_name='admission_deadline',
        lookup_expr='lte',
        label='Дедлайн до или в эту дату'
    )
    admission_deadline_after = django_filters.DateFilter(
        field_name='admission_deadline',
        lookup_expr='gte',
        label='Дедлайн после или в эту дату'
    )

    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte', label='минимальная стоимость')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte', label='максимальная стоимость')

    formats = django_filters.BaseInFilter(field_name='format', lookup_expr='in', label='формат обучения')

    certificates = django_filters.BaseInFilter(
        field_name='academic_requirements__name',
        lookup_expr='in',
        label='Названия требований (список)'
    )

    # certificates_grades = django_filters.CharFilter(
    #     method='filter_multiple_requirements',
    #     label='Требования (название:порог через запятую)'
    # )

    # def filter_multiple_requirements(self, queryset, name, value):
    #     requirements = value.split(',')
    #     q_objects = Q()
    #     for req in requirements:
    #         if ':' in req:
    #             req_name, req_treshold = req.split(':')
    #             q_objects |= Q(
    #                 academic_requirements__name__iexact=req_name.strip(),
    #                 academic_requirements__treshold__lte=float(req_treshold)
    #             )
    #     return queryset.filter(q_objects).distinct()

    class Meta:
        model = Program
        fields = [
            'countries',
            'cities',
            'names',
            'specialty_groups',
            'languages',
            'admission_deadline_before',
            'admission_deadline_after',
            'price_min',
            'price_max',
            'formats',
            'certificates',
            # 'certificates_grades',
        ]



