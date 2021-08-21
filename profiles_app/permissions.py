from rest_framework import permissions


class OwnerOrAdminOnly(permissions.BasePermission):
    isAuthenticated = permissions.IsAuthenticatedOrReadOnly()
    isAdmin = permissions.IsAdminUser()

    def has_permission(self, request, view):
        return self.isAuthenticated.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if bool(request.user and request.user.is_authenticated):
            return request.user.id == obj.user.id
        return self.isAdmin.has_permission(request, view)


class DeviceOwnerOrAdminOnly(permissions.BasePermission):
    isAuthenticated = permissions.IsAuthenticated()
    isAdmin = permissions.IsAdminUser()

    def has_permission(self, request, view):
        if view.action == 'update_own' or request.method in permissions.SAFE_METHODS:
            return self.isAuthenticated.has_permission(request, view)
        return self.isAdmin.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if self.isAdmin.has_permission(request, view):
            return True
        return request.user.id == obj.user.id
