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
