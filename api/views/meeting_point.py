from rest_framework.viewsets import ModelViewSet
from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.meeting_point import IsCommunityMember, IsCommunityModerator
from api.serializers import MeetingPointSerializer, MeetingPointCreateSerializer
from core.models import MeetingPoint, Member


class MeetingPointViewSet(ModelViewSet):
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
    serializer_class = MeetingPointSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        if self.request.method == 'POST':
            return [IsCommunityMember()]
        return [IsCommunityModerator()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = MeetingPointCreateSerializer
        return serializer_class

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        user_communities = Member.objects.filter(user=user, status='1').values('community')
        return self.model.objects.filter(location__community__in=user_communities)
