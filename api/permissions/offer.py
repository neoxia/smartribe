from rest_framework.permissions import BasePermission
from api.authenticate import AuthUser
from core.models import Member, Request


class IsJWTSelfAndConcerned(BasePermission):
    """

    """
    def has_permission(self, request, view):
        user, response = AuthUser().authenticate(request)
        data = request.DATA
        if not user:
            return False
        if 'user' not in data or 'request' not in data:
            return False
        if user.id != data['user']:
            return False
        if not Request.objects.filter(id=data['request']).exists():
            return False
        request = Request.objects.get(id=data['request'])
        user_communities = Member.objects.filter(user=user).values('community')
        linked_users = Member.objects.filter(community__in=user_communities).values('user')
        if request.user not in linked_users:
            return False
        return True