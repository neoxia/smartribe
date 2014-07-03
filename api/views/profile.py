from rest_framework import viewsets
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner, IsJWTSelf
from core.models import Profile
from api.serializers.serializers import ProfileCreateSerializer
from api.serializers.serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    Inherits standard characteristics from ModelViewSet:
            | **Endpoint**: /profiles/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTOwner
            |       - GET : IsJWTAuthenticated
            |       - POST : IsJWTSelf
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
