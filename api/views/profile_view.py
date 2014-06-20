from rest_framework import viewsets
from api.permissions import IsJWTAuthenticated, IsJWTOwner, IsJWTSelf
from core.models import Profile
from api.serializers.serializers import ProfileCreateSerializer
from api.serializers.serializers import ProfileSerializer


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
