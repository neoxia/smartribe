from django.db.models import Q
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.permissions.common import IsJWTAuthenticated
from api.permissions.message import IsConcernedByOffer
from api.serializers.message import MessageSerializer, MessageCreateSerializer
from api.utils.notifier import Notifier
from core.models import Message


class MessageViewSet(mixins.CreateModelMixin,
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
    model = Message
    serializer_class = MessageSerializer
    filter_fields = ('user__id', 'offer__id')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsConcernedByOffer()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = MessageCreateSerializer
        return serializer_class

    def pre_save(self, obj):
        if self.request.method == 'POST':
            obj.user = self.request.user

    def post_save(self, obj, created=False):
        if self.request.method == 'POST':
            Notifier.notify_new_message(obj)

    def get_queryset(self):
        return self.model.objects.filter( Q(offer__user=self.request.user) |
                                          Q(offer__request__user=self.request.user)).order_by('creation_date')
