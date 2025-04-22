from django.db.models import Max, Min
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .constants import LanguageChoices, FormatChoices, DegreeChoices
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
            'languages': LanguageChoices.values,
            'degrees': DegreeChoices.values,
            'formats': FormatChoices.values,
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
                                   distinct()
        },
            'languages': filtered_queryset.values_list("language", flat=True).
                                   distinct(),
            'formats': filtered_queryset.values_list("format", flat=True).
            distinct(),
            'max_price': filtered_queryset.aggregate(Max('price'))['price__max'],
            'min_price': filtered_queryset.aggregate(Min('price'))['price__min'],
            'countries': filtered_queryset.values_list("education_place__city__country__id", flat=True).distinct(),
            'cities': filtered_queryset.values_list("education_place__city__id", flat=True).distinct(),
            'specialty_groups': filtered_queryset.values_list("specialities__specialty_group__id", flat=True).distinct(),
            'deadline_min': filtered_queryset.aggregate(Min('admission_deadline'))['admission_deadline__min'],
            'certificates': filtered_queryset.values_list("academic_requirements__name", flat=True).distinct(),
            'deadline_max': filtered_queryset.aggregate(Max('admission_deadline'))['admission_deadline__max'],

        }

        response_data = Response(data=[[serializer.data], [custom_data]])



        return response_data


