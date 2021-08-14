from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit thier own profile"""

    def has_object_permission(self, request, view, obj):
        """Check user is trying to edit thier own profile"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update thier onw status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update thier own status"""
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id


class DevicesViewPermissions(permissions.BasePermission):
    def __init__(self):
        self.isAdmin = permissions.IsAdminUser()
        self.isAuthenticated = permissions.IsAuthenticated()

    def has_permission(self, request, view):
        if view.action == 'update_own' or request.method in permissions.SAFE_METHODS:
            return self.isAuthenticated.has_permission(request, view)
        return self.isAdmin.has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        if self.isAdmin.has_permission(request, view):
            return True
        return request.user.id == obj.user.id
