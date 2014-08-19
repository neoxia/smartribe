from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.authenticate import AuthUser
from api.serializers import LocalCommunitySerializer
from api.serializers.location import LocationCreateSerializer
from api.views.community import CommunityViewSet
from core.models import LocalCommunity, Location


class LocalCommunityViewSet(CommunityViewSet):
    """
    Inherits properties and methods from CommunityViewSet.

            | **Endpoint**: /local_communities/
            |   For methods inherited form 'CommunityViewSet', just replace endpoint '/communities/'
            |   by /local_communities/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsCommunityOwner
            |       - GET or POST: IsJWTAuthenticated
            |       - PUT or PATCH : IsCommunityModerator

    """
    model = LocalCommunity
    serializer_class = LocalCommunitySerializer
    search_fields = ('name', 'description', 'address__city')

    # Member actions



    # Moderator actions

    @action(methods=['POST'])
    def delete_location(self, request, pk=None):
        """
        Delete a location.

                | **permission**: Community moderator
                | **endpoint**: /local_communities/{id}/delete_location/
                | **method**: POST
                | **attr**:
                |       - id (integer)
                | **http return**:
                |       - 200 OK
                |       - 400 Bad request
                |       - 401 Unauthorized
                |       - 403 Forbidden
                |       - 404 Not found
                | **data return**:
                |       None
                | **other actions**:
                |       None
        """
        user, _ = AuthUser().authenticate(request)
        if pk is None:
            return Response({'detail': 'Missing community index.'}, status=status.HTTP_404_NOT_FOUND)
        if not self.model.objects.filter(id=pk).exists():
            return Response({'detail': 'Wrong pk parameter'}, status=status.HTTP_404_NOT_FOUND)
        loc_community = self.model.objects.get(id=pk)
        if not self.check_moderator_permission(user, loc_community):
            return Response({'detail': 'Community member rights required.'}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.DATA
        if 'id' not in data:
            return Response({'detail': 'No location id provided.'}, status=status.HTTP_400_BAD_REQUEST)
        if not Location.objects.filter(community=pk, id=data['id']).exists():
            return Response({'detail': 'No such location.'}, status=status.HTTP_401_UNAUTHORIZED)
        location = Location.objects.get(id=data['id'])
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)