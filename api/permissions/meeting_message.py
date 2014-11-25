from rest_framework.permissions import BasePermission

from api.authenticate import AuthUser
from core.models import Offer, MeetingPoint, Member, Meeting


class IsConcernedByMeeting(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        if 'user' not in data:
            return False
        if user.id != data['user']:
            return False
        if 'offer' not in data:
            return False
        if not Offer.objects.filter(id=data['offer']).exists():
            return False
        o = Offer.objects.get(id=data['offer'])
        if user != o.user and user != o.request.user:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if user != obj.offer.user and user != obj.offer.request.user:
            return False
        return True
