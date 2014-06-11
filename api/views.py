import hashlib
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework_jwt import authentication
import sys
from core.models import Profile, Community
from rest_framework import viewsets
from api.serializers import UserSerializer
from api.serializers import GroupSerializer
from api.serializers import TokenSerializer
from api.serializers import PermissionSerializer
from api.serializers import ProfileSerializer
from api.serializers import CommunitySerializer
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.hashers import make_password
from rest_framework import status


class UserViewSet(viewsets.ViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = User.objects.all()
    #serializer = UserSerializer
    permission_classes = [permissions.AllowAny]
    model = User

    #def list(self, request):
        #queryset = User.objects.all()
        #serializer = UserSerializer(queryset, many=True)
        #return Response(serializer.data)

    def create(self, request):
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])
        serial_user = UserSerializer(data=data)
        if serial_user.is_valid():
            serial_user.save()
            return Response(serial_user.data, status=status.HTTP_201_CREATED)
        return Response(serial_user.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        queryset = User.objects.all()
        try:
            user = get_object_or_404(queryset, pk=pk)
        except (TypeError, ValueError):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data, content_type='application/json')






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


@csrf_exempt
def Create_User(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        data['password'] = make_password(data['password'])
        serial_user = UserSerializer(data = data)
        if serial_user.is_valid():
            serial_user.save()
            return JSONResponse(serial_user.data)

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        del data['password']
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)