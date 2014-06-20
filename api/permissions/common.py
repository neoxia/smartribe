from rest_framework.permissions import BasePermission

from api.authenticate import AuthUser


"""
Include API common permissions
"""

class IsJWTAuthenticated(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, _ = AuthUser().authenticate(request)
        if not user:
            return False
        else:
            return True


class IsJWTOwner(BasePermission):
    """

    """
    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if user.id == obj.user.id:
            return True
        else:
            return False


class IsJWTSelf(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        elif user.id != data['user']:
            return False
        else:
            return True