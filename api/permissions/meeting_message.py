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
        if 'meeting' not in data:
            return False
        if not Meeting.objects.filter(id=data['meeting']).exists():
            return False
        m = Meeting.objects.get(id=data['meeting'])
        if user != m.offer.user and user != m.offer.request.user:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if user != obj.meeting.offer.user and user != obj.meeting.offer.request.user:
            return False
        return True
