from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.meeting import IsConcernedByMeeting
from api.serializers import MeetingSerializer, MeetingCreateSerializer
from api.utils.notifier import Notifier
from api.views.abstract_viewsets.custom_viewset import CustomViewSet
from core.models import Meeting


class MeetingViewSet(CustomViewSet):
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
    create_serializer_class = MeetingCreateSerializer
    serializer_class = MeetingSerializer
    filter_fields = ('offer__id', 'user__id', 'status')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsConcernedByMeeting()]

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return self.model.objects.filter(Q(offer__user=user) | Q(offer__request__user=user))

    def pre_save(self, obj):
        self.set_auto_user(obj)

    def post_save(self, obj, created=False):
        if self.request.method == 'POST':
            Notifier.notify_new_meeting(obj)

    @action(methods=['POST'])
    def accept_meeting(self, request, pk=None):
        """
        Accept a meeting

                | **permission**: IsConcernedByMeeting and Not meeting creator
                | **endpoint**: /meetings/{id}/accept_meeting/
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                |       - 404 Not Found
                | **data return**:
                |       - Modified meeting object
                | **other actions**:
                |       None
        """
        obj, response = self.validate_object(request, pk)
        if not obj:
            return response
        user, _ = AuthUser().authenticate(self.request)
        if user == obj.user:
            return Response({'detail': 'Operation not allowed.'}, status.HTTP_403_FORBIDDEN)
        obj.status = 'A'
        obj.save()
        serializer = MeetingSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def refuse_meeting(self, request, pk=None):
        """
        Validate a meeting

                | **permission**: IsConcernedByMeeting and Not meeting creator
                | **endpoint**: /meetings/{id}/refuse_meeting/
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                |       - 404 Not Found
                | **data return**:
                |       - Modified meeting object
                | **other actions**:
                |       None
        """
        obj, response = self.validate_object(request, pk)
        if not obj:
            return response
        user, _ = AuthUser().authenticate(self.request)
        if user == obj.user:
            return Response({'detail': 'Operation not allowed.'}, status.HTTP_403_FORBIDDEN)
        obj.status = 'R'
        obj.save()
        serializer = MeetingSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST'])
    def validate_meeting(self, request, pk=None):
        """
        Validate a meeting

                | **permission**: IsConcernedByMeeting
                | **endpoint**: /meetings/{id}/validate_meeting/
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                |       - 404 Not Found
                | **data return**:
                |       - Modified meeting object
                | **other actions**:
                |       None
        """
        obj, response = self.validate_object(request, pk)
        if not obj:
            return response
        user, _ = AuthUser().authenticate(self.request)
        if user != obj.offer.user and user != obj.offer.request.user:
            return Response({'detail': 'Operation not allowed.'}, status.HTTP_403_FORBIDDEN)
        if obj.status != 'A':
            return Response({'detail': 'Status must be \'Accepted\' to validate.'}, status.HTTP_403_FORBIDDEN)
        obj.is_validated = True
        obj.save()
        serializer = MeetingSerializer(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
