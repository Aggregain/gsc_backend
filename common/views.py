from django.db.models import Max, Min
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import LANGUAGE_TR, FORMAT_TR, DEGREE_TR
from .filters import ProgramFilter
from .models import Country, City, EducationPlace, Program, SpecialtyGroup
from .serializers import CountrySerializer, EducationPlaceSerializer, CitySerializer, ProgramSerializer, \
    SpecialtyGroupSerializer


class RosterView(APIView):
    permission_classes = [AllowAny,]
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
    # page_size = 30

    def list(self, request, *args, **kwargs):

        base_queryset = self.get_queryset()


        filtered_queryset = self.filter_queryset(base_queryset)



        serializer = self.get_serializer(filtered_queryset, many=True)


        custom_data = {'filters': {
                        'programs': filtered_queryset.
                                   values_list("name", flat=True).
                                   distinct(),
            'languages': filtered_queryset.exclude(language__isnull=True).order_by("language").
            values_list("language", flat=True).distinct("language"),
            'formats': filtered_queryset.exclude(format__isnull=True).order_by("format").values_list("format",
                                                                                                     flat=True).
            distinct("format"),
            'max_price': filtered_queryset.aggregate(Max('price'))['price__max'] or 0,
            'min_price': filtered_queryset.aggregate(Min('price'))['price__min'] or 0,
            'countries': filtered_queryset.exclude(education_place__city__country__id__isnull=True).order_by(
                "education_place__city__country__id").values_list("education_place__city__country__id",
                                                                  flat=True).distinct(
                "education_place__city__country__id"),
            'cities': filtered_queryset.exclude(education_place__city__id__isnull=True).order_by(
                "education_place__city__id").values_list("education_place__city__id", flat=True).distinct(
                "education_place__city__id"),
            'specialty_groups': filtered_queryset.exclude(specialities__specialty_group__id__isnull=True).order_by(
                "specialities__specialty_group__id").values_list("specialities__specialty_group__id",
                                                                 flat=True).distinct(
                "specialities__specialty_group__id"),
            'deadline_min': filtered_queryset.aggregate(Min('admission_deadline'))['admission_deadline__min'] or 0,
            'certificates': filtered_queryset.exclude(academic_requirements__name__isnull=True).order_by(
                "academic_requirements__name").values_list("academic_requirements__name", flat=True).distinct(
                "academic_requirements__name"),
            'deadline_max': filtered_queryset.aggregate(Max('admission_deadline'))['admission_deadline__max'] or 0,
        },


        }

        response_data = Response(data={'programs':serializer.data, 'filters':custom_data})



        return response_data


