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
from api.serializers import UserSerializer, ProfileCreateSerializer, CommunityCreateSerializer, MemberSerializer, \
    MemberCreateSerializer
from api.serializers import ProfileSerializer
from api.serializers import UserCreateSerializer
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
        serial_user = UserCreateSerializer(data=data)
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

    def list(self, request):
        user, response = AuthUser().authenticate(request)
        if not user:
            return response
        serializer = UserSerializer(user)
        return Response(serializer.data)




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


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows profiles to be viewed or edited.
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
        elif self.request.method == 'POST':
            return [IsJWTSelf()]
        else:
            return [IsJWTOwner()]


class CommunityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows communities to be viewed or edited.
    """
    model = Community
    serializer_class = CommunitySerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = CommunityCreateSerializer
        return serializer_class

    def get_permissions(self):
        """
        An authenticated user can create a new community or see existing communities.
        Only owner or moderator can modify an existing community.
        """
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsJWTAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsCommunityModerator()]
        else:
            return [IsCommunityOwner()]

    def create(self, request, *args, **kwargs):
        """
        Overrides standard 'create' method to simultaneously add an owner member
        """
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            user, _ = AuthUser().authenticate(request)
            owner = Member(user=user, community=self.object, role="0", status="1")
            owner.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MemberViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows members to be viewed or edited.
    """
    model = Member
    serializer_class = MemberSerializer

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = MemberCreateSerializer
        return serializer_class

    def get_permissions(self):
        """
        An authenticated user can register itself as a new member of a community.
        Only a community owner or moderator can list or modify member status.
        Only a community owner can modify a member role.
        """
        if self.request.method == 'POST':
            return [IsJWTSelf()]
        elif self.request.method == 'GET':
            return [IsCommunityModerator()]
        else:
            return [IsCommunityOwner()]

    def create(self, request, *args, **kwargs):
        """
        Overrides standard 'create' method to avoid multiple identical members creation
        """
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            data = request.DATA
            if Member.objects.filter(user=data['user'], community=data['community']).exists():
                member = Member.objects.get(user=data['user'], community=data['community'])
                return Response(MemberSerializer(member).data, status=HTTP_200_OK)
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)