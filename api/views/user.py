from datetime import timedelta, tzinfo, timezone
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils.datetime_safe import datetime
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.serializers.serializers import UserSerializer
from api.serializers.serializers import UserCreateSerializer
from api.authenticate import AuthUser
from core.models.activation_token import ActivationToken
import core.utils
from core.models.password_recovery import PasswordRecovery


class UserViewSet(viewsets.ViewSet):
    """ Default permission: Any """
    permission_classes = [permissions.AllowAny]
    model = User

    def create(self, request):
        """ Create user:

                | **permission**: any
                | **endpoint**: /users/
                | **method**: POST
                | **attr**:
                |       - username: string (required)
                |       - password: string (required)
                |       - email: string (required)
                |       - groups: array
                | **http return**:
                |       - 201 Created successfully
                |       - 400 Bad request
                | **data return**:
                |       - username: string
                |       - email: string
                |       - groups: array

        """
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])
        data['is_active'] = False
        serial_user = UserCreateSerializer(data=data)
        if serial_user.is_valid():
            serial_user.save()
            token = ActivationToken(user=User.objects.get(username=data['username']),
                                    token=core.utils.gen_temporary_token())
            token.save()
            #send_mail(
                #'SmarTribe registration',
                #'TO BE COMPLETED',
                #'noreply@smartri.be',
                #data['email'],
                #fail_silently=False
            #)
            return Response(serial_user.data, status=status.HTTP_201_CREATED)
        return Response(serial_user.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', ])
    def confirm_registration(self, request, pk=None):
        """ Confirm user registration:

                | **permission**: any
                | **endpoint**: /users/{id}/confirm_registration
                | **method**: POST
                | **attr**:
                |       - token: string (required)
                | **http return**:
                |       - 200 OK
                |       - 400 Bad request
                | **data return**:
                |       - None

        """
        if not User.objects.filter(id=pk).exists():
            return Response({"detail":"Wrong URL"}, status=status.HTTP_400_BAD_REQUEST)
        data = JSONParser().parse(request)
        if not 'token' in data:
            return Response({"detail":"Missing token"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=pk)
        if not ActivationToken.objects.filter(user=user, token=data['token']):
            return Response({"detail":"Activation error"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        ActivationToken.objects.get(user=user, token=data['token']).delete()
        return Response(status=status.HTTP_200_OK)




    def retrieve(self, request, pk=None):
        """ Get user:

                | **permission**: authenticated, get self
                | **endpoint**: /users/{id}/
                | **method**: GET
                | **http return**:
                |       - 200 OK
                |       - 403 Forbidden
                | **data return**:
                |       - url: resource
                |       - username: string
                |       - email: string
                |       - groups: array

        """

        user, response = AuthUser().authenticate(request)
        forbidden = status.HTTP_403_FORBIDDEN
        if not user:
            return response
        elif str(user.id) != pk:
            return Response({"detail": "Access denied"}, status=forbidden)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """ Update user

                | **permission**: authenticated, get self
                | **endpoint**: /users/{id}/
                | **method**: PUT, (PATCH?)
                | **http return**:
                |       - 201 Created
                |       - 403 Forbidden
                | **data return**:
                |       - url: resource
                |       - username: string
                |       - email: string
                |       - groups: array

        """
        user, response = AuthUser().authenticate(request)
        forbidden = status.HTTP_403_FORBIDDEN
        if not user:
            return response
        elif str(user.id) != pk:
            return Response({"detail": "Access denied"}, status=forbidden)
        data = JSONParser().parse(request)
        if 'password' in data:
            data['password'] = make_password(data['password'])
        serial_user = UserSerializer(user, data=data, partial=True)
        if serial_user.is_valid():
            serial_user.save()
            return Response(serial_user.data, status=status.HTTP_201_CREATED)
        return Response(serial_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        """ **NOT A LIST** Get current authenticated user:

                | **permission**: authenticated, get self
                | **endpoint**: /users/
                | **method**: GET
                | **http return**:
                |       - 200 OK
                |       - 403 Forbidden
                | **data return**:
                |       - url: resource
                |       - username: string
                |       - email: string
                |       - groups: array

        """

        user, response = AuthUser().authenticate(request)
        if not user:
            return response
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @action(methods=['POST', ])
    def recover_password(self, request, pk=None):
        """ Recover password

                | **permission**: any
                | **endpoint**: /users/0/recover_password
                | **method**: POST
                | **attr**:
                |       - email: string (required)
                | **http return**:
                |       - 200 OK
                |       - 400 Bad request
                |       - 401 Unauthorized
                | **data return**:
                |       None
                | **other actions**:
                |       - Sends an email with a password recovery token

        """
        data = JSONParser().parse(request)
        if 'email' in data:
            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                ip = core.utils.get_client_ip(request)
                list = PasswordRecovery.objects.filter(user=user)
                if list.count() >= 2:
                    last_pr = list.order_by('-pk')[1]
                    fr = timezone(timedelta(hours=1), "Europe/Rome")
                    delta = datetime.now(tz=fr) - last_pr.request_datetime
                    if delta < timedelta(minutes=5):
                        return Response({"detail":"Try again after 5 min"}, status=status.HTTP_401_UNAUTHORIZED)
                token = core.utils.gen_temporary_token()
                pr = PasswordRecovery(user=user, token=token, ip_address=ip)
                pr.save()
                send_mail('SmarTribe password recovery', token, 'noreply@smartri.be', [user.email], fail_silently=False)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({"detail":"Unknown email address"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"Email address required"}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST', ])
    def set_new_password(self, request, pk=None):
        """ Set a new password, using password recovery token

                | **permission**: any
                | **endpoint**: /users/{token}/set_new_password
                | **method**: POST
                | **attr**:
                |       - password: string (required)
                | **http return**:
                |       - 200 OK
                |       - 400 Bad request
                | **data return**:
                |       None
                | **other actions**:
                |       - Sends an email with a password recovery token

        """
        token = pk
        data = JSONParser().parse(request)
        if token is not None:
            if 'password' in data:
                if PasswordRecovery.objects.filter(token=token).exists():
                    user = PasswordRecovery.objects.get(token=token).user
                    user.password = make_password(data['password'])
                    user.save()
                    PasswordRecovery.objects.filter(user=user).delete()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"detail":"No password renewal request"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"detail":"Password required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"Token required"}, status=status.HTTP_400_BAD_REQUEST)