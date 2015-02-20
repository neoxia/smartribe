from rest_framework.permissions import BasePermission

from api.authenticate import AuthUser
from core.models import Offer, MeetingPoint, Member, Meeting


class IsConcernedByMeeting(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if 'pk' in view.kwargs:
            if Meeting.objects.filter(id=view.kwargs['pk']).exists():
                return self.has_object_permission(request, view, Meeting.objects.get(id=view.kwargs['pk']))
        if not user:
            return False
        if 'offer' not in data:
            return False
        if 'meeting_point' not in data:
            return False
        if not Offer.objects.filter(id=data['offer']).exists():
            return False
        of = Offer.objects.get(id=data['offer'])
        if user != of.user and user != of.request.user:
            return False
        if not MeetingPoint.objects.filter(id=data['meeting_point']).exists():
            return False
        mp = MeetingPoint.objects.get(id=data['meeting_point'])
        if not Member.objects.filter(user=user, community=mp.location.community, status='1').exists():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        user, response = AuthUser().authenticate(request)
        if not user:
            return False
        if user != obj.offer.user and user != obj.offer.request.user:
            return False
        return True
