from django.db.models import Q
from rest_framework.permissions import BasePermission

from api.authenticate import AuthUser
from core.models import Member


# Includes permissions for community and member objects

# PERMISSIONS ON COMMUNITIES

class IsCommunityOwner(BasePermission):
    """
    Owner's rights on 'Community' objects
    """
    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        elif Member.objects.filter(
                user=user.id,
                community=obj.id,
                status="1",
                role="0"
        ).exists():
            return True
        else:
            return False


class IsCommunityModerator(BasePermission):
    """
    Moderator's rights on 'Community' objects
    """
    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        elif Member.objects.filter(
                Q(user=user.id),
                Q(community=obj.id),
                Q(status="1"),
                Q(role="1") | Q(role="0")
        ).exists():
            return True
        else:
            return False


# PERMISSIONS ON MEMBERS

class IsOwnerAndNotBanned(BasePermission):
    """

    """
    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        elif obj.user.id == user.id and obj.status != "2":
            return True
        else:
            return False


class IsMemberManager(BasePermission):
    """

    """
    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        elif Member.objects.filter(
                user=user.id,
                community=obj.community,
                status="1",
                role="1"
        ).exists() and obj.role == "2":
            data = request.DATA
            if 'role' in data:
                if data['role'] == "2":
                    return True
                else:
                    return False
            else:
                return True
        elif Member.objects.filter(
                user=user.id,
                community=obj.community,
                status="1",
                role="0"
        ).exists():
            return True
        else:
            return False