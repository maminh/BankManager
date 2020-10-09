from rest_framework.permissions import BasePermission


class HaveAccountPermission(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'account')
