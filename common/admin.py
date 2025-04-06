from django.contrib import admin
from .models import City, Country, EducationPlace
from unfold.admin import ModelAdmin
from django.contrib.sites.models import Site

admin.site.unregister(Site)

@admin.register(Site)
class SiteAdmin(ModelAdmin):
    ...

@admin.register(Country)
class CountryAdmin(ModelAdmin):
    ...

@admin.register(City)
class CityAdmin(ModelAdmin):
    ...

@admin.register(EducationPlace)
class EducationPlaceAdmin(ModelAdmin):
    ...