from rest_framework import permissions


class OwnerOrAdmin(permissions.BasePermission):
    is_Authenticated = permissions.IsAuthenticatedOrReadOnly()

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return self.is_Authenticated.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return obj.user == request.user
