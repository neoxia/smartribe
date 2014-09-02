from rest_framework.viewsets import ModelViewSet

from api.authenticate import AuthUser
from api.permissions.location import IsCommunityMember, IsCommunityModerator
from api.serializers.location import LocationSerializer, LocationCreateSerializer, TransportLocationCreateSerializer
from core.models import Member, Location, Community, TransportCommunity


class LocationViewSet(ModelViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /locations/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsCommunityModerator
            |       - GET or POST : IsCommunityMember

    """
    model = Location
    serializer_class = LocationSerializer

    def get_permissions(self):
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsCommunityMember()]
        return [IsCommunityModerator()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            data = self.request.data
            if 'community' in data and Community.objects.filter(id=data['community']).exists():
                c = Community.objects.get(id=data['community'])
                try:
                    c.transportCommunity
                except TransportCommunity.DoesNotExist:
                    serializer_class = LocationCreateSerializer
                else:
                    serializer_class = TransportLocationCreateSerializer
            else:
                serializer_class = LocationCreateSerializer
        return serializer_class

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        user_communities = Member.objects.filter(user=user, status='1').values('community')
        return Location.objects.filter(location__in=user_communities)
