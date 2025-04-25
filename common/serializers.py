from rest_framework.serializers import ModelSerializer

from .models import City, Country, EducationPlace, Program, AcademicRequirement, SpecialtyGroup


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', ]


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country', 'name']


class EducationPlaceSerializer(ModelSerializer):
    class Meta:
        model = EducationPlace
        fields = '__all__'


class ProgramBaseSerializer(ModelSerializer):

    class Meta:
        model = Program
        fields = '__all__'


class EducationPlaceDetailSerializer(EducationPlaceSerializer):
    programs = ProgramBaseSerializer(many=True, read_only=True, source='degrees')

    class Meta(EducationPlaceSerializer.Meta):
        ...


class AcademicRequirementSerializer(ModelSerializer):
    class Meta:
        model = AcademicRequirement
        fields = '__all__'


class SpecialtyGroupSerializer(ModelSerializer):
    class Meta:
        model = SpecialtyGroup
        fields = '__all__'


class ProgramSerializer(ProgramBaseSerializer):
    academic_requirements = AcademicRequirementSerializer(many=True, read_only=True)
    education_place = EducationPlaceSerializer(read_only=True)

    class Meta(ProgramBaseSerializer.Meta):
        ...
