from rest_framework import viewsets
from rest_framework.response import Response
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner, IsJWTSelf
from api.serializers import ProfileCreateSerializer, ProfileSerializer
from core.models import Profile
from rest_framework import status


class ProfileViewSet(viewsets.ModelViewSet):
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
    model = Profile
    serializer_class = ProfileSerializer
    filter_fields = ('user__id', )

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

    # FIXME : Allow GET only for members sharing at least one community ?