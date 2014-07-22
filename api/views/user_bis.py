from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from api.authenticate import AuthUser

from api.permissions.common import IsJWTAuthenticated, IsJWTMe
from api.serializers.serializers import UserCreateSerializer, UserSerializer, UserPublicSerializer
from core.models import ActivationToken, PasswordRecovery
from rest_framework import status
import core.utils
from datetime import timedelta, tzinfo, timezone, datetime
from rest_framework import filters
import django_filters
from rest_framework import generics


class UserFilter(django_filters.FilterSet):
    """
    Specific search filter for users
    """
    username = django_filters.CharFilter(name='username', lookup_type='contains')

    class Meta:
        model = User
        fields = ['username', ]


class LoginViewSet(viewsets.ViewSet):
    """
    Login endpoint
    """
    permission_classes = [AllowAny]
    model = User

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


class UserListView(generics.ListAPIView):
    serializer_class = UserPublicSerializer
    permission_classes = [AllowAny,]

    def search(self):
        return self.get_queryset()

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        #username = self.kwargs['username']
        #return User.objects.filter(username=username)

        queryset = User.objects.all()
        username = self.request.QUERY_PARAMS.get('username', None)
        if username is not None:
            queryset = queryset.filter(username=username)
        return queryset



class UserBisViewSet(viewsets.ModelViewSet):
    """
    Inherits standard characteristics from ModelViewSet:
            | **Endpoint**: /profiles/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTOwner
            |       - GET : IsJWTAuthenticated
            |       - POST : IsJWTSelf
    Overrides standard pre_delete() method to destroy address object simultaneously.
    """
    model = User
    serializer_class = UserSerializer
    filter_class = UserFilter

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        user, _ = AuthUser().authenticate(self.request)
        if self.request.method == 'GET' and 'pk' not in self.kwargs:
            serializer_class = UserPublicSerializer
        elif self.request.method == 'GET' and not self.object == user:
            serializer_class = UserPublicSerializer
        elif self.request.method == 'POST':
            serializer_class = UserCreateSerializer
        return serializer_class

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        elif self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [IsJWTMe()]

    def pre_save(self, obj):
        super().pre_save(obj)
        if obj.password:
            obj.password = make_password(obj.password)
        if self.request.method == 'POST':
            obj.is_active = False

    def post_save(self, obj, created=False):
        if self.request.method == 'POST':
            token = ActivationToken(user=User.objects.get(username=obj.username),
                                    token=core.utils.gen_temporary_token())
            token.save()
            send_mail('SmarTribe registration', token.token, 'noreply@smartri.be', [obj.email], fail_silently=False)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

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
            return Response({"detail": "Wrong URL"}, status=status.HTTP_400_BAD_REQUEST)
        data = JSONParser().parse(request)
        if not 'token' in data:
            return Response({"detail": "Missing token"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(id=pk)
        if not ActivationToken.objects.filter(user=user, token=data['token']).exists():
            return Response({"detail": "Activation error"}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.save()
        ActivationToken.objects.get(user=user, token=data['token']).delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST', ])
    def recover_password(self, request, pk=None):
        """ Recover password

                | **permission**: any
                | **endpoint**: /users/0/recover_password/
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
        if 'email' not in data:
            return Response({"detail": "Email address required"}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(email=data['email']).exists():
            return Response({"detail": "Unknown email address"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.get(email=data['email'])
        ip = core.utils.get_client_ip(request)
        user_list = PasswordRecovery.objects.filter(user=user)
        if user_list.count() >= 2:
            last_pr = user_list.order_by('-pk')[1]
            fr = timezone(timedelta(hours=1), "Europe/Rome")
            delta = datetime.now(tz=fr) - last_pr.request_datetime
            if delta < timedelta(minutes=5):
                return Response({"detail": "Try again after 5 min"}, status=status.HTTP_401_UNAUTHORIZED)
        token = core.utils.gen_temporary_token()
        pr = PasswordRecovery(user=user, token=token, ip_address=ip)
        pr.save()
        send_mail('SmarTribe password recovery', token, 'noreply@smartri.be', [user.email], fail_silently=False)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['POST', ])
    def set_new_password(self, request, pk=None):
        """ Set a new password, using password recovery token

                | **permission**: any
                | **endpoint**: /users/{token}/set_new_password/
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
        if token is None:
            return Response({"detail": "Token required"}, status=status.HTTP_400_BAD_REQUEST)
        if not 'password' in data:
            return Response({"detail": "Password required"}, status=status.HTTP_400_BAD_REQUEST)
        if not PasswordRecovery.objects.filter(token=token).exists():
            return Response({"detail": "No password renewal request"}, status=status.HTTP_400_BAD_REQUEST)
        user = PasswordRecovery.objects.get(token=token).user
        user.password = make_password(data['password'])
        user.save()
        PasswordRecovery.objects.filter(user=user).delete()
        return Response(status=status.HTTP_200_OK)