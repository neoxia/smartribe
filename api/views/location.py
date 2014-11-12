from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.location import IsCommunityMember, IsCommunityModerator
from api.serializers.location import LocationSerializer, LocationCreateSerializer, TransportLocationCreateSerializer
from core.models import Member, Location, Community, TransportCommunity


class LocationViewSet(ReadOnlyModelViewSet):
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
        """if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsCommunityMember()]
        return [IsCommunityModerator()]"""
        return [IsJWTAuthenticated()]

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
        return Location.objects.filter(community__in=user_communities)

    @link(permission_classes=[IsJWTAuthenticated()])
    def get_shared_locations(self, request, pk=None):
        """
         Get locations shared by two users
        """
        user, _ = AuthUser().authenticate(request)
        data = request.QUERY_PARAMS
        if 'other_user' not in data:
            return Response({'detail': 'Missing other_user id'}, status=status.HTTP_400_BAD_REQUEST)
        if not User.objects.filter(pk=data['other_user']).exists():
            return Response({'detail': 'No other_user with this id'}, status=status.HTTP_400_BAD_REQUEST)
        other_user = User.objects.get(pk=data['other_user'])
        user_communities = Member.objects.filter(user=user).values('community')
        other_user_communities = Member.objects.filter(user=other_user).values('community')
        shared_communities = user_communities and other_user_communities
        shared_locations = Location.objects.filter(community__in=shared_communities)
        page = self.paginate_queryset(shared_locations)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)