from rest_framework import permissions

from applications.constants import StatusChoices


class ApplicationEditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.status == StatusChoices.DRAFT:
            return obj.owner == request.user or request.user.is_staff
        return request.user.is_staff