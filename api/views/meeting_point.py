from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import link
from rest_framework import status
from rest_framework.response import Response
from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.meeting_point import IsCommunityMember, IsCommunityModerator
from api.serializers import MeetingPointSerializer, MeetingPointCreateSerializer
from api.views.abstract_viewsets.custom_viewset import CustomViewSet
from core.models import MeetingPoint, Member, Location, Community
from core.models.offer import Offer


class MeetingPointViewSet(CustomViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /meeting_points/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsCommunityModerator
            |       - GET : IsJWTAuthenticated
            |       - POST : IsCommunityMember

    """
    model = MeetingPoint
    create_serializer_class = MeetingPointCreateSerializer
    serializer_class = MeetingPointSerializer
    filter_fields = ('location',)
    search_fields = ('name', 'description')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        if self.request.method == 'POST':
            return [IsCommunityMember()]
        return [IsCommunityModerator()]

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        user_communities = Member.objects.filter(user=user, status='1').values('community')
        return self.model.objects.filter(location__community__in=user_communities)

    @link(permission_classes=[IsJWTAuthenticated()])
    def get_shared_meeting_points(self, request, pk=None):
        """
         Get relevant meeting points for an offer
        """
        user, _ = AuthUser().authenticate(request)
        data = request.QUERY_PARAMS
        if 'offer' not in data:
            return Response({'detail': 'Missing offer id'}, status=status.HTTP_400_BAD_REQUEST)
        if not Offer.objects.filter(pk=data['offer']).exists():
            return Response({'detail': 'No offer with this id'}, status=status.HTTP_400_BAD_REQUEST)
        offer = Offer.objects.get(pk=data['offer'])
        req = offer.request
        if user != offer.user and user != req.user:
            return Response({'detail': 'Operation not allowed'}, status=status.HTTP_403_FORBIDDEN)
        if user == offer.user:
            other_user = req.user
        else:
            other_user = offer.user
        if req.community:
            locations = Location.objects.filter(community=req.community)
            meeting_points = MeetingPoint.objects.filter(location__in=locations)
        else:
            user_communities = Member.objects.filter(user=user, status='1').values('community')
            other_user_communities = Member.objects.filter(user=other_user, status='1').values('community')
            shared_communities = Community.objects.filter(Q(id__in=user_communities) & Q(id__in=other_user_communities))
            shared_locations = Location.objects.filter(community__in=shared_communities)
            meeting_points = MeetingPoint.objects.filter(location__in=shared_locations)
        serializer = self.get_paginated_serializer(meeting_points)
        return Response(serializer.data, status=status.HTTP_200_OK)