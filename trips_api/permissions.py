from rest_framework import permissions

class CreateOwnTrip(permissions.BasePermission):
    """Allow user to edit thier own trips"""
    
    def has_permission(self, request, view):
        return False

    def has_object_permission(self,request,view,obj):
        """Check user is trying to edit thier own profile"""
        if request.method in ['GET']:            
            return True

        return obj.userId.id == request.user.id
