from django.db.models import Max, Min
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import ProgramFilter
from .models import Country, City, EducationPlace, Program
from .serializers import CountrySerializer, EducationPlaceSerializer, CitySerializer, ProgramSerializer


class RosterView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        countries = Country.objects.all()
        cities = City.objects.select_related('country').all()
        education_places = EducationPlace.objects.select_related('city').all()
        return Response({
            'countries': CountrySerializer(countries, many=True).data,
            'cities': CitySerializer(cities, many=True).data,
            'education_places': EducationPlaceSerializer(education_places, many=True).data
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
        .all()
    )
    serializer_class = ProgramSerializer
    filterset_class = ProgramFilter
    ordering_fields = "__all__"
    permission_classes = [IsAuthenticated]
    page_size = 30

    def list(self, request, *args, **kwargs):

        base_queryset = self.get_queryset()


        filtered_queryset = self.filter_queryset(base_queryset)


        page = self.paginate_queryset(filtered_queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response_data = self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(filtered_queryset, many=True)
            response_data = Response(serializer.data)

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
            'countries': filtered_queryset.values_list("education_place__city__country__name", flat=True).distinct(),
            'cities': filtered_queryset.values_list("education_place__city__name", flat=True).distinct(),
            'specialty_groups': filtered_queryset.values_list("specialities__specialty_group__name", flat=True).distinct(),
            'deadline_min': filtered_queryset.aggregate(Min('admission_deadline'))['admission_deadline__min'],

            'deadline_max': filtered_queryset.aggregate(Max('admission_deadline'))['admission_deadline__max'],

        }


        response_data.data.append(custom_data)


        return response_data


