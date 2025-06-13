
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django_celery_beat.models import (
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)
from django_celery_results.models import TaskResult, GroupResult
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm

from .forms import AccountChangeForm, AccountCreationForm
from .models import Account, Attachment

admin.site.unregister(PeriodicTask)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(TaskResult)
admin.site.unregister(GroupResult)

admin.site.unregister(Group)




@admin.register(Account)
class AccountAdmin(BaseUserAdmin, ModelAdmin):
    form = AccountChangeForm
    add_form = AccountCreationForm
    change_password_form = AdminPasswordChangeForm

    fieldsets = (
        (None, {"fields": ("password",)}),
        (
            _("Personal info"),
            {"fields": ("first_name", "second_name", "last_name", "birth_date", "avatar", "email", "degree")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name", "second_name", "last_name", "birth_date", "avatar", "email", "password1",
                    "password2",  "is_active", "is_staff", "is_superuser",
                ),
            },
        ),
    )
    list_display = ("email", "second_name", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active",)
    search_fields = ("first_name", "last_name", "second_name", "email")
    ordering = ("created_at",)


@admin.register(Attachment)
class AttachmentAdmin(ModelAdmin):
    ...