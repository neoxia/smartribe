from django.db.models import Q
from rest_framework.permissions import BasePermission
from api.authenticate import AuthUser
from core.models import Location, Member


class IsCommunityMember(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        if 'location' not in data:
            return False
        if not Location.objects.filter(id=data['location']).exists():
            return False
        loc = Location.objects.get(id=data['location'])
        if not Member.objects.filter(user=user, community=loc.community, status='1').exists():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if not Member.objects.filter(user=user, community=obj.location.community, status='1').exists():
            return False
        return True


class IsCommunityModerator(BasePermission):
    """

    """
    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if not Member.objects.filter(Q(user=user),
                                     Q(community=obj.location.community),
                                     Q(status='1'),
                                     Q(role='0') | Q(role='1')).exists():
            return False
        return True