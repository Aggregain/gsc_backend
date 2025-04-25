from django.db.models import Max, Min
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import LANGUAGE_TR, FORMAT_TR, DEGREE_TR, CERTS
from .filters import ProgramFilter
from .models import Country, City, EducationPlace, Program, SpecialtyGroup
from .serializers import CountrySerializer, EducationPlaceSerializer, CitySerializer, ProgramSerializer, \
    SpecialtyGroupSerializer, EducationPlaceDetailSerializer


class RosterView(APIView):
    permission_classes = [AllowAny, ]

    def get(self, request):
        countries = Country.objects.all()
        cities = City.objects.select_related('country').all()
        education_places = EducationPlace.objects.select_related('city').all()
        specialty_groups = SpecialtyGroup.objects.all()
        return Response({
            'countries': CountrySerializer(countries, many=True).data,
            'cities': CitySerializer(cities, many=True).data,
            'education_places': EducationPlaceSerializer(education_places, many=True).data,
            'specialty_groups': SpecialtyGroupSerializer(specialty_groups, many=True).data,
            'languages': LANGUAGE_TR,
            'degrees': DEGREE_TR,
            'formats': FORMAT_TR,
            'certificates': CERTS,
        })


class ProgramListApiView(ListAPIView):
    queryset = (
        Program.objects.select_related(
            "education_place",
            "education_place__city",
            "education_place__city__country",
        )
        .prefetch_related(
            "specialities__specialty_group",
            "academic_requirements",
            "specialities",
            "education_place__deadlines",
            "academic_requirements",
        )
        .filter(education_place__is_for_admission=True).order_by("name")
    )

    serializer_class = ProgramSerializer
    filterset_class = ProgramFilter
    ordering_fields = "__all__"
    permission_classes = [IsAuthenticated]

    # permission_classes = [AllowAny]


    def list(self, request, *args, **kwargs):
        base_queryset = self.get_queryset()
        filtered_queryset = self.filter_queryset(base_queryset)
        params = request.query_params
        ordering_param = params.get('ordering')
        if ordering_param:
            try:
                fields = [field.strip() for field in ordering_param.split(',')]
                ordered_queryset = filtered_queryset.order_by(*fields)
            except Exception:
                ordered_queryset = filtered_queryset  # fallback
        else:
            ordered_queryset = filtered_queryset
        serializer = self.get_serializer(ordered_queryset, many=True)


        agg_data = base_queryset.aggregate(
            max_price=Max('price'),
            min_price=Min('price'),
            deadline_min=Min('admission_deadline'),
            deadline_max=Max('admission_deadline'),
        )
        is_countries_selected = 'countries' in params
        filters = {
            'countries': base_queryset.exclude(education_place__city__country__id__isnull=True).order_by(
                "education_place__city__country__id").values_list("education_place__city__country__id",
                                                                  flat=True).distinct(
                "education_place__city__country__id"),
            'cities': filtered_queryset.exclude(education_place__city__id__isnull=True).order_by(
                "education_place__city__id").values_list("education_place__city__id", flat=True).distinct(
                "education_place__city__id") if is_countries_selected else base_queryset.exclude(education_place__city__id__isnull=True).order_by(
                "education_place__city__id").values_list("education_place__city__id", flat=True).distinct(
                "education_place__city__id"),
            'names': base_queryset.order_by("name").
            values_list("name", flat=True).distinct("name"),
            'specialty_groups': base_queryset.exclude(specialities__specialty_group__id__isnull=True).order_by(
                "specialities__specialty_group__id").values_list("specialities__specialty_group__id",
                                                                 flat=True).distinct(
                "specialities__specialty_group__id"),
            'languages': base_queryset.exclude(language__isnull=True).order_by("language").
            values_list("language", flat=True).distinct("language"),
            'deadlines': {'max': agg_data['deadline_max'] or 0,
                          'min': agg_data['deadline_min'] or 0},
            'prices': {'min': agg_data['min_price'] or 0,
                       'max': agg_data['max_price'] or 0},
            'formats': base_queryset.exclude(format__isnull=True).order_by("format").values_list("format",
                                                                                                     flat=True).
            distinct("format"),


            'certificates': base_queryset.exclude(academic_requirements__name__isnull=True).order_by(
                "academic_requirements__name").values_list("academic_requirements__name", flat=True).distinct(
                "academic_requirements__name"),

        }

        response_data = Response(data={'programs': serializer.data, 'filters': filters})
        return response_data





class UniversityRetrieveApiView(RetrieveAPIView):
    queryset = (EducationPlace.objects.
                select_related('city', 'city__country').
                prefetch_related('degrees','expenses', 'specialities', 'deadlines',
                                 'specialities__specialty_group').
                filter(is_for_admission=True))
    serializer_class = EducationPlaceDetailSerializer
    permission_classes = [IsAuthenticated,]
    # permission_classes = [AllowAny, ]
