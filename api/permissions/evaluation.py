from rest_framework.permissions import BasePermission

from api.authenticate import AuthUser
from core.models import Offer, MeetingPoint, Member, Meeting


class IsEvaluator(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        if 'meeting' not in data:
            return False
        if not Meeting.objects.filter(id=data['meeting']).exists():
            return False
        m = Meeting.objects.get(id=data['meeting'])
        if user != m.offer.request.user or not m.is_validated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if user != obj.meeting.offer.user or not obj.meeting.is_validated:
            return False
        return True
