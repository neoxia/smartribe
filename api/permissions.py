from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from api.authenticate import AuthUser

class IsJWTAuthenticated(BasePermission):

    def has_permission(self, request, view):
        user, _ = AuthUser().authenticate(request)
        if not user:
            return False
        else:
            return True

class IsJWTOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if obj.user == user.url:
            return True
        else:
            return False

class IsJSelf(BasePermission):

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        elif str(user.id) != obj.pk:
            return False
        else:
            return True

