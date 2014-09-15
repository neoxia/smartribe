from datetime import timedelta, timezone, datetime

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import Avg, Min, Max
from rest_framework import viewsets
from rest_framework.decorators import action, link
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
import django_filters

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTMe
from api.serializers.serializers import UserCreateSerializer, UserSerializer, UserPublicSerializer
from core.models import ActivationToken, PasswordRecovery, Evaluation
import core.utils


class UserFilter(django_filters.FilterSet):
    """
    Specific search filter for users
    """
    username = django_filters.CharFilter(name='username', lookup_type='contains')

    class Meta:
        model = User
        fields = ['username', ]


class UserViewSet(viewsets.ModelViewSet):
    """
    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /users/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTMe
            |       - GET : IsJWTAuthenticated
            |       - POST : AllowAny

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
            send_mail('SmarTribe registration',
                      'https://demo.smartri.be/'+token.token+'/confirm_registration/',
                      'noreply@smartri.be',
                      [obj.email],
                      fail_silently=False)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(methods=['POST', ])
    def confirm_registration(self, request, pk=None):
        """ Confirm user registration:

                | **permission**: any
                | **endpoint**: /users/{token}/confirm_registration
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 400 Bad request
                | **data return**:
                |       None

        """
        """if not User.objects.filter(id=pk).exists():
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
        return Response(status=status.HTTP_200_OK)"""
        token = pk
        if token is None:
            return Response({"detail": "Missing token"}, status=status.HTTP_400_BAD_REQUEST)
        if not ActivationToken.objects.filter(token=token).exists():
            return Response({"detail": "Activation error"}, status=status.HTTP_400_BAD_REQUEST)
        user = ActivationToken.objects.get(token=token).user
        user.is_active = True
        user.save()
        ActivationToken.objects.get(token=token).delete()
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
        send_mail('SmarTribe password recovery',
                  'https://demo.smartri.be/password/:'+token+'/edit',
                  'noreply@smartri.be',
                  [user.email],
                  fail_silently=False)
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

    @link(permission_classes=[IsJWTAuthenticated])
    def get_my_user(self, request, pk=None):
        """
        Get current authenticated user:

                | **permission**: authenticated, get self
                | **endpoint**: /users/0/get_my_user/
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

    @link(permission_classes=[IsJWTAuthenticated])
    def get_user_evaluation(self, request, pk=None):
        """
        Get evaluation information for a specific user:

                | **permission**: authenticated
                | **endpoint**: /users/{id}/get_user_evaluation/
                | **method**: GET
                | **http return**:
                |       - 200 OK
                |       - 403 Forbidden
                |       - 404 Not found
                | **data return**:
                |       - average_eval (float)
                |       - min_eval(integer)
                |       - max_eval(integer)

        """
        if pk is None:
            return Response({'detail': 'Id requested in URL.'}, status.HTTP_404_NOT_FOUND)
        if not self.model.objects.filter(id=pk).exists():
            return Response({'detail': 'No such object.'}, status.HTTP_404_NOT_FOUND)
        obj = self.model.objects.get(id=pk)
        if not Evaluation.objects.filter(meeting__offer__user=obj).exists():
            eval = {}
        else:
            eval = Evaluation.objects.filter(meeting__offer__user=obj).aggregate(average_eval=Avg('mark'),
                                                                                 min_eval=Min('mark'),
                                                                                 max_eval=Max('mark'))
        return Response(eval, status=status.HTTP_200_OK)
