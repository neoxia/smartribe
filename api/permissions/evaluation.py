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
        if 'offer' not in data:
            return False
        if not Offer.objects.filter(id=data['offer']).exists():
            return False
        o = Offer.objects.get(id=data['offer'])
        if user != o.request.user:
            return False
        return True


class IsEvaluationAuthor(BasePermission):
    """ """
    def has_object_permission(self, request, view, obj):
        if not request.user:
            return False
        if request.user != obj.offer.request.user:
            return False
        return True
