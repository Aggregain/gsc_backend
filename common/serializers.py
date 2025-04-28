from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import City, Country, EducationPlace, Program, AcademicRequirement, SpecialtyGroup, Deadline, Expense, \
    Specialty


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

class ExpensesSerializer(ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class AcademicRequirementSerializer(ModelSerializer):
    class Meta:
        model = AcademicRequirement
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



class SpecialtySerializer(ModelSerializer):
    group_name = SerializerMethodField()
    program_name = SerializerMethodField()
    class Meta:
        model = Specialty
        exclude = ['specialty_group', 'program']

    def get_group_name(self, obj):
        return obj.specialty_group.name

    def get_program_name(self, obj):
        return obj.program.name




class ProgramDetailSerializer(ProgramBaseSerializer):
    expenses = ExpensesSerializer(many=True, read_only=True,)
    deadlines = DeadlineSerializer(many=True, read_only=True)
    academic_requirements = AcademicRequirementSerializer(many=True, read_only=True)
    class Meta(ProgramBaseSerializer.Meta):
        ...


class EducationPlaceDetailSerializer(EducationPlaceSerializer):
    programs = ProgramDetailSerializer(many=True, read_only=True, source='degrees')
    specialties = SpecialtySerializer(many=True, read_only=True,)
    class Meta(EducationPlaceSerializer.Meta):
        ...


class SpecialtyGroupSerializer(ModelSerializer):
    class Meta:
        model = SpecialtyGroup
        fields = '__all__'


class ProgramSerializer(ProgramBaseSerializer):
    academic_requirements = AcademicRequirementSerializer(many=True, read_only=True)
    education_place = EducationPlaceSerializer(read_only=True)

    class Meta(ProgramBaseSerializer.Meta):
        ...
