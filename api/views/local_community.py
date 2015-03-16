from django.utils.translation import ugettext as _
from math import cos, radians
from rest_framework.decorators import link
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from api.permissions.common import IsJWTAuthenticated
from api.permissions.community import IsCommunityOwner, IsCommunityModerator
from api.serializers import LocalCommunitySerializer
from api.views.community import CommunityViewSet
from core.models import LocalCommunity


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
            | **Extra-methods:** (HTTP method / permission)
            |       - Memberships management
            |           - join_community (POST / Authenticated)
            |           - list_my_memberships (GET / Authenticated)
            |           - leave_community (POST / Authenticated)
            |           - retrieve_members (GET / Moderator)
            |           - accept_member (POST / Moderator)
            |           - ban_member (POST / Moderator)
            |           - promote_moderator (POST / Owner)
            |       - Locations management
            |           - add_location (POST / Member)
            |           - list_locations (GET / Member)
            |           - search_locations (GET / Member)
            |           - delete_location (POST / Moderator)

    """
    model = LocalCommunity
    serializer_class = LocalCommunitySerializer
    search_fields = ('name', 'description', 'city')

    def get_permissions(self):
        """
        An authenticated user can create a new community or see existing communities.
        Only owner or moderator can modify an existing community.
        """
        if self.request.method == 'DELETE':
            return [IsCommunityOwner()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsCommunityModerator()]
        elif self.request.method == 'GET' and 'list_communities_around_me' in self.request.get_full_path():
            return [AllowAny()]
        else:
            return [IsJWTAuthenticated()]

    @link()
    def list_communities_around_me(self, request, pk=None):
        """ List communities around a central GPS point with a radius (km) given as parameter """
        data = request.QUERY_PARAMS
        if not 'gps_x' in data or not 'gps_y' in data or not 'radius' in data:
            Response({_('detail'): _('Missing GPS coordinates or search radius.')}, status=status.HTTP_400_BAD_REQUEST)
        gps_x = float(data['gps_x'])
        gps_y = float(data['gps_y'])
        radius = float(data['radius'])
        delta_y = radius / 111
        delta_x = radius / (111 * cos(radians(gps_y)))
        communities = LocalCommunity.objects.filter(gps_x__gt=gps_x-delta_x,
                                                    gps_x__lt=gps_x+delta_x,
                                                    gps_y__gt=gps_y-delta_y,
                                                    gps_y__lt=gps_y+delta_y)
        page = self.paginate_queryset(communities)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(communities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
