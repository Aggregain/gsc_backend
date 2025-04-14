from rest_framework import permissions

class IsOwnerOrAdminPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
       return (obj.account == request.user or
               request.user.is_superuser or
               request.user.is_staff)
