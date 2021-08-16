from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    is_Authenticated = permissions.IsAuthenticatedOrReadOnly()

    def has_permission(self, request, view):
        return self.is_Authenticated.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user


class ModeratedByAdminOnly(permissions.BasePermission):
    is_Authenticated = permissions.IsAuthenticatedOrReadOnly()

    def has_permission(self, request, view):
        if self.is_Authenticated.has_permission(request, view):
            return request.user.is_staff
        return False
