from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import MeetingMessage


class MeetingMessageCreateSerializer(serializers.ModelSerializer):
    """

    """

    class Meta:
        model = MeetingMessage
        exclude = ('creation_date')


class MeetingMessageSerializer(ReportableModelSerializer):
    """

    """

    class Meta:
        model = MeetingMessage
        read_only_fields = ('meeting', 'user', 'creation_date')