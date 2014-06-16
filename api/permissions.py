from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from api.authenticate import AuthUser
from core.models import Member


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
        if not user:
            return False
        if user.id == obj.user.id:
            return True
        else:
            return False

class IsJWTSelf(BasePermission):

    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        elif user.id != data['user']:
            return False
        else:
            return True

class IsCommunityOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        else:
            try:
                Member.objects.get(user=user.id, community=obj.id, status="1", role="0")
                return True
            except:
                return False



class IsCommunityModerator(BasePermission):
    pass

class IsCommunityMember(BasePermission):
    pass