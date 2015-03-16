from django.db.models import Max
from api.serializers import TransportCommunitySerializer
from api.views.community import CommunityViewSet
from core.models import TransportCommunity, Location


class TransportCommunityViewSet(CommunityViewSet):
    """
    Inherits properties and methods from CommunityViewSet.

            | **Endpoint**: /transport_communities/
            |   For methods inherited form 'CommunityViewSet', just replace endpoint '/communities/'
            |   by /transport_communities/
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
            |           - add_location (POST / Member) - WARNING : 'index' parameter mandatory
            |           - list_locations (GET / Member)
            |           - search_locations (GET / Member)
            |           - delete_location (POST / Moderator)

    """
    model = TransportCommunity
    serializer_class = TransportCommunitySerializer
    search_fields = ('name', 'description', 'departure', 'via', 'arrival')

    def pre_add_location(self, data, community):
        # Case with no index
        if 'index' not in data:
            raise Exception
        index = data['index']
        # Case with negative index
        if index < 0:
            raise Exception
        locations = Location.objects.filter(community=community)
        # Case with no existing location
        if not locations.exists() and index is not 0:
            raise Exception
        # Case with index too high
        max_index = locations.aggregate(Max('index'))['index__max']
        if locations.exists() and index > max_index + 1:
            raise Exception
        loc_to_reindex = locations.filter(index__gte=index)
        for l in loc_to_reindex:
            l.index += 1
            l.save()

    def pre_delete_location(self, location, community):
        loc_to_reindex = Location.objects.filter(community=community, index__gt=location.index)
        for l in loc_to_reindex:
            l.index -= 1
            l.save()
        pass
