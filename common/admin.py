from django.contrib import admin
from django.contrib.sites.models import Site
from django.db import models
from django.forms import DateInput
from django.urls.base import reverse
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.import_export.forms import ImportForm, SelectableFieldsExportForm

from .models import (
    City, Country, EducationPlace, Deadline, Program,
    SpecialtyGroup, Specialty, Expense, AcademicRequirement
)
from .resources import EducationPlaceResource

admin.site.unregister(Site)


class ProgramInline(TabularInline):
    fields = ('name', 'duration_years', 'language', 'format', 'edit_link')
    model = Program
    extra = 0
    readonly_fields = ('edit_link',)

    def edit_link(self, obj):
        if obj.pk:
            url = reverse('admin:common_program_change', args=[obj.pk])
            return format_html('<a class="button" href="{}" target="_blank">Редактировать</a>', url)
        return ''

    edit_link.short_description = 'Редактировать'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('education_place')


class DeadlineInline(TabularInline):
    model = Deadline
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('program')


class ExpenseInline(TabularInline):
    model = Expense
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('program')


class AcademicRequirementInline(TabularInline):
    model = AcademicRequirement
    extra = 0

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('program')


class SpecialtyInline(TabularInline):
    fields = ('name', 'program', 'specialty_group', 'duration', 'price', 'admission_deadline', 'edit_link')
    model = Specialty
    extra = 0
    readonly_fields = ('edit_link',)

    def edit_link(self, obj):
        if obj.pk:
            url = reverse('admin:common_specialty_change', args=[obj.pk])
            return format_html('<a class="button" href="{}" target="_blank">Редактировать</a>', url)
        return ''

    edit_link.short_description = 'Редактировать'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('specialty_group', 'program')

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'program' and request:
            try:
                parent_id = request.resolver_match.kwargs.get('object_id')
                if parent_id:
                    from .models import Program
                    field.queryset = Program.objects.filter(education_place_id=parent_id)
            except Exception:
                pass
        return field


@admin.register(Country)
class CountryAdmin(ModelAdmin):
    ...


@admin.register(City)
class CityAdmin(ModelAdmin):
    list_per_page = 20
    search_fields = ('name',)
    list_display = ('name', 'id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('country')


@admin.register(EducationPlace)
class EducationPlaceAdmin(ImportExportModelAdmin, ModelAdmin):
    list_per_page = 20
    list_display = ('name', 'get_country', 'city', 'rating',)
    search_fields = ('name',)
    exclude = ('prices_data',)

    resource_class = EducationPlaceResource

    import_form_class = ImportForm
    export_form_class = SelectableFieldsExportForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('city', 'city__country')

    @admin.display(description='Страна')
    def get_country(self, obj):
        return obj.city.country.name




@admin.register(Program)
class ProgramAdmin(ModelAdmin):
    inlines = [AcademicRequirementInline, ExpenseInline, SpecialtyInline,]
    exclude = ('specialty_durations', 'description_academic', 'description_prices')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('education_place')


@admin.register(SpecialtyGroup)
class SpecialtyGroupAdmin(ModelAdmin):
    ...


@admin.register(Specialty)
class SpecialtyAdmin(ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('specialty_group', 'program__education_place')
