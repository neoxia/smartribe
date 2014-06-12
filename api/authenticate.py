from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework import status


class AuthUser:
    def authenticate(self, request):
        try:
            auth_data = JSONWebTokenAuthentication().authenticate(request)
            if not auth_data:
                msg = {"detail": "Missing credentials"}
                raise exceptions.AuthenticationFailed(msg)
            else:
                user, token = auth_data
        except exceptions.AuthenticationFailed as ex:
            response = Response(ex.detail, status=status.HTTP_401_UNAUTHORIZED)
            return None, response
        return user, Response({"detail": "Auth success"})
