from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth.hashers import make_password
from rest_framework import status
from core.models import Profile, Community
from api.serializers import UserSerializer
from api.serializers import GroupSerializer
from api.serializers import TokenSerializer
from api.serializers import PermissionSerializer
from api.serializers import ProfileSerializer
from api.serializers import CommunitySerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions

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
        try:
            if not JSONWebTokenAuthentication().authenticate(request):
                raise exceptions.AuthenticationFailed({"detail":"Missing credentials"})
            user,_ = JSONWebTokenAuthentication().authenticate(request)
        except exceptions.AuthenticationFailed as ex:
            return Response(ex.detail, status=status.HTTP_401_UNAUTHORIZED)
        if str(user.id) != pk:
            return Response({"detail":"Access denied"}, status=status.HTTP_403_FORBIDDEN)
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
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class CommunityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

