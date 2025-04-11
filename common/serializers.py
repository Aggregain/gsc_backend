from rest_framework.serializers import ModelSerializer, Serializer
from .models import City, Country, EducationPlace


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name']


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class EducationPlaceSerializer(ModelSerializer):
    class Meta:
        model = EducationPlace
        fields = ['id', 'name']

