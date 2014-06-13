from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import status
from api.permissions import IsJWTAuthenticated, IsJWTOwner
from core.models import Profile, Community
from api.serializers import UserSerializer
from api.serializers import ProfileSerializer
from api.serializers import ProfileCreateSerializer
from api.serializers import GroupSerializer
from api.serializers import TokenSerializer
from api.serializers import PermissionSerializer
from api.serializers import CommunitySerializer

from api.authenticate import AuthUser


class UserViewSet(viewsets.ViewSet):

    permission_classes = [permissions.AllowAny]
    model = User

    def create(self, request):
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])
        serial_user = UserSerializer(data=data)
        if serial_user.is_valid():
            serial_user.save()
            return Response(serial_user.data, status=status.HTTP_201_CREATED)
        return Response(serial_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user, response = AuthUser().authenticate(request)
        forbidden = status.HTTP_403_FORBIDDEN
        if not user:
            return response
        elif str(user.id) != pk:
            return Response({"detail": "Access denied"}, status=forbidden)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
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


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TokenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Token.objects.all()
    serializer_class = TokenSerializer


class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    model = Profile
    serializer_class = ProfileSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = ProfileCreateSerializer
        return serializer_class

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        else:
            return [IsJWTOwner()]

    """
    def create(self, request):
        data = JSONParser().parse(request)
        serial_profile = ProfileSerializer(data=data)
        if serial_profile.is_valid():
            serial_profile.save()
            return Response(serial_profile.data, status=status.HTTP_201_CREATED)
        return Response(serial_profile.errors, status=status.HTTP_400_BAD_REQUEST)
    """


class CommunityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

