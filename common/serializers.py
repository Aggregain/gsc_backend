
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import City, Country, EducationPlace, Program, AcademicRequirement, SpecialtyGroup


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

class SpecialtyGroupSerializer(ModelSerializer):
    class Meta:
        model = SpecialtyGroup
        fields = '__all__'

class ProgramSerializer(ModelSerializer):
    academic_requirements = AcademicRequirementSerializer(many=True, read_only=True)
    university_rating = SerializerMethodField()
    class Meta:
        model = Program
        fields = '__all__'

    def get_university_rating(self, obj):
        return str(obj.education_place.rating)