from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsActiveUser(BasePermission):
    """
    Allows access only to active users.
    """

    def has_permission(self, request, view):
        return bool(request.user) and bool(request.user.is_authenticated) and bool(request.user.is_active)


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as a admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and request.user.is_admin
        )
