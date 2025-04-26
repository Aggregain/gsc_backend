from rest_framework.serializers import ModelSerializer, Serializer, SerializerMethodField

from .models import City, Country, EducationPlace, Program, AcademicRequirement, SpecialtyGroup, Deadline, Expense


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ['id', 'name', ]


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country', 'name']

class DeadlineSerializer(ModelSerializer):
    class Meta:
        model = Deadline
        fields = '__all__'

class EducationPlaceSerializer(ModelSerializer):
    class Meta:
        model = EducationPlace
    city_name = SerializerMethodField()
    country_name = SerializerMethodField()

    class Meta:
        model = EducationPlace
        exclude = ['city', ]

    def get_city_name(self, obj):
        return obj.city.name

    def get_country_name(self, obj):
        return obj.city.country.name


class ProgramBaseSerializer(ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class ExpensesSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class EducationPlaceDetailSerializer(EducationPlaceSerializer):
    programs = ProgramBaseSerializer(many=True, read_only=True, source='degrees')
    deadlines = DeadlineSerializer(many=True)
    expenses = ExpensesSerializer(many=True)
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
