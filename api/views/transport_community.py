from rest_framework.decorators import link, action
from api.permissions.community import IsCommunityModerator, IsCommunityMember
from api.serializers import TransportCommunitySerializer
from api.views.community import CommunityViewSet
from core.models import TransportCommunity


class TransportCommunityViewSet(CommunityViewSet):
    """
    Inherits properties from CommunityViewSet

            | **Endpoint**: /transport_communities/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsCommunityOwner
            |       - GET or POST: IsJWTAuthenticated
            |       - PUT or PATCH : IsCommunityModerator

    """
    model = TransportCommunity
    serializer_class = TransportCommunitySerializer
    search_fields = ('name', 'description', 'departure', 'via', 'arrival')

    def insert_location(self, request, pk=None):
        pass

    @link(permission_classes=[IsCommunityModerator])
    def list_stops(self, request, pk=None):
        """

        """


    @action(methods=['POST'], permission_classes=[IsCommunityMember])
    def add_stop(self, request, pk=None):
        """

        """
