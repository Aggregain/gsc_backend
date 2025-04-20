from rest_framework.serializers import ModelSerializer, Serializer
from .models import City, Country, EducationPlace, Program, AcademicRequirement


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name',]


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country', 'name']


class EducationPlaceSerializer(ModelSerializer):
    class Meta:
        model = EducationPlace
        fields = ['id', 'city' ,'name', 'description', 'is_for_admission']


class AcademicRequirementSerializer(ModelSerializer):
    class Meta:
        model = AcademicRequirement
        fields = '__all__'

class ProgramSerializer(ModelSerializer):
    academic_requirements = AcademicRequirementSerializer(many=True, read_only=True)
    class Meta:
        model = Program
        fields = '__all__'