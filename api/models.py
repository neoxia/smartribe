import base64
import hashlib
from django.contrib.auth.models import User
from django.db import models
from rest_framework import authentication
from api.error_views import forbidden, not_found


class Auth(authentication.BaseAuthentication):
    user = None
    response = None

    def __init__(self, request):
        if request.META.get('HTTP_AUTHORIZATION') is None:
            self.response = forbidden(request)
        else:
            r = base64.b64decode(request.META.get('HTTP_AUTHORIZATION')[6:])
            r = r.split(':')
            username = r[0]
            password = r[1]
            if not username:
                return None
            try:
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                self.response = not_found(request)
            password_digest = hashlib.sha1(password).hexdigest()
            if user.password != password_digest:
                self.response = forbidden(request)
                self.user = user

    def is_admin(self):
        return (self.user.role == 'admin')

    def is_authentified(self):
        return (self.user != None)

