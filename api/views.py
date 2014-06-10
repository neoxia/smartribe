import hashlib
from django.contrib.auth.models import User, Group, Permission
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from core.models import Profile, Community
from rest_framework import viewsets
from api.serializers import UserSerializer
from api.serializers import GroupSerializer
from api.serializers import TokenSerializer
from api.serializers import PermissionSerializer
from api.serializers import ProfileSerializer
from api.serializers import CommunitySerializer
from rest_framework.renderers import JSONRenderer



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
        # data['password'] = hashlib.sha256(data['password'])
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