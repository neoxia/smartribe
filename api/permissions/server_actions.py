from rest_framework.permissions import BasePermission
from django.conf import settings


class HasAllowedIp(BasePermission):
    """  """
    def has_permission(self, request, view):
        ip_address = request.META.get('REMOTE_ADDR')
        if ip_address in settings.ALLOWED_IP:
            return True
        return False