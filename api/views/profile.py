from rest_framework import viewsets
from rest_framework.response import Response
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner, IsJWTSelf
from core.models import Profile
from api.serializers.serializers import ProfileCreateSerializer
from api.serializers.serializers import ProfileSerializer
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

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Overrides standard "Destroy" method, to destroy address simultaneously

                | **permission**: owner
                | **endpoint**: /profiles/{id}/
                | **method**: DELETE
                | **attr**:
                |       None
                | **http return**:
                |       - 204 No Content
                |       - 400 Bad request
                | **data return**:
                |       - url: resource
                |       - name: string
                |       - description: string
                |       - created_date : date
                |       - auto_accept_member: boolean (true|false)
        """
        # TODO : Verify if profile exists
        obj = self.get_object()
        if Profile.objects.filter(id=pk).exists():
            address = Profile.objects.get(id=pk).address
            address.delete()
        self.pre_delete(obj)
        obj.delete()
        self.post_delete(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)