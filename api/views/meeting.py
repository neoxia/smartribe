from django.db.models import Q

from rest_framework.viewsets import ModelViewSet

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.meeting import IsConcernedByMeeting
from api.serializers import MeetingSerializer, MeetingCreateSerializer
from core.models import Member, Meeting


class MeetingViewSet(ModelViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /meetings/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsConcernedByMeeting
            |       - GET : IsJWTAuthenticated
            | **Notes**:
            |       - GET response restricted to 'Meeting' objects linked with user

    """
    model = Meeting
    serializer_class = MeetingSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsConcernedByMeeting()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = MeetingCreateSerializer
        return serializer_class

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return self.model.objects.filter(Q(offer__user=user) | Q(offer__request__user=user))
