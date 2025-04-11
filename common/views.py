from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CountrySerializer, EducationPlaceSerializer, CitySerializer
from .models import Country, City, EducationPlace
from rest_framework.permissions import AllowAny


class RosterView(APIView):
    permission_classes = [AllowAny,]
    def get(self, request):
        countries = Country.objects.all()
        cities = City.objects.all()
        education_places = EducationPlace.objects.all()
        return Response({
            'countries': CountrySerializer(countries, many=True).data,
            'cities': CitySerializer(cities, many=True).data,
            'education_places': EducationPlaceSerializer(education_places, many=True).data
        })
