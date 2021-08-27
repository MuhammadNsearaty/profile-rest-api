from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    is_authenticated = permissions.IsAuthenticatedOrReadOnly()

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.is_authenticated.has_permission(request, view) and request.user.is_staff
