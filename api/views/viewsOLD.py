from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.status import HTTP_200_OK
from api.permissions import IsJWTAuthenticated, IsJWTOwner, IsJWTSelf, IsCommunityOwner, IsCommunityModerator
from core.models import Profile, Community, Member
from api.serializers.serializers import UserSerializer, ProfileCreateSerializer, CommunityCreateSerializer, MemberSerializer, \
    MemberCreateSerializer
from api.serializers.serializers import ProfileSerializer
from api.serializers.serializers import UserCreateSerializer
from api.serializers.serializers import GroupSerializer
from api.serializers.serializers import TokenSerializer
from api.serializers.serializers import PermissionSerializer
from api.serializers.serializers import CommunitySerializer
from api.authenticate import AuthUser



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
    API endpoint that allows permissions to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


