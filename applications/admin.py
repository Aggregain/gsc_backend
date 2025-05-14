from django.contrib import admin

from .models import Application
from unfold.admin import ModelAdmin
from accounts.models import Account

@admin.register(Application)
class ApplicationAdmin(ModelAdmin):

    sortable_by = ['created_at']
    readonly_fields = ['owner',]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('owner', 'assignee', 'program')


    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'assignee':
            kwargs["queryset"] = Account.objects.filter(is_staff=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)