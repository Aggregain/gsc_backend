from rest_framework import permissions

from applications.constants import StatusChoices


class ApplicationEditPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.status in [StatusChoices.DRAFT, StatusChoices.FOR_REVISION]:
            return obj.owner == request.user
        return request.user.is_staff