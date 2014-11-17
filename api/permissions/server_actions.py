from rest_framework.permissions import BasePermission
from api.authenticate import AuthUser
from core.models import Member, Request
from smartribe.settings import ALLOWED_IP


class HasAllowedIp(BasePermission):
    """

    """
    def has_permission(self, request, view):
        ip_address = request.META.get('REMOTE_ADDR')
        if ip_address in ALLOWED_IP:
            return True
        return False