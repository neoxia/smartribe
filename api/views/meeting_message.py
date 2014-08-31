from django.db.models import Q
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.meeting_message import IsConcernedByMeeting
from api.serializers.meeting_message import MeetingMessageSerializer, MeetingMessageCreateSerializer
from core.models import MeetingMessage


class MeetingMessageViewSet(mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.ListModelMixin,
                            GenericViewSet):
    """

    Inherits standard characteristics from ModelViewSet for Create, List and Retrieve actions:

            | **Endpoint**: /meeting_messages/
            | **Methods**: GET / POST / OPTIONS
            | **Permissions**:
            |       - Default : IsConcernedByMeeting
            | **Notes**:
            |       - GET response restricted to 'MeetingMessage' objects linked with user

    """
    model = MeetingMessage
    serializer_class = MeetingMessageSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsConcernedByMeeting()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = MeetingMessageCreateSerializer
        return serializer_class

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return self.model.objects.filter( Q(meeting__offer__user=user) | Q(meeting__offer__request__user=user))
