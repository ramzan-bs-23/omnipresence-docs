from rest_framework import permissions


class IsFrontline(permissions.BasePermission):
    """Allows access only to frontline users."""

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role == 'frontline'


class IsAdministrator(permissions.BasePermission):
    """Allows access only to administrators."""

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role == 'administrator'


class IsManager(permissions.BasePermission):
    """Allows access only to managers/viewers."""

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role == 'manager'


class IsAdministratorOrManager(permissions.BasePermission):
    """Allows access to administrators and managers."""

    def has_permission(self, request):
        return request.user.is_authenticated and request.user.role in ['administrator', 'manager']
