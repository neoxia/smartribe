from rest_framework import serializers
from core.models import Meeting


class MeetingCreateSerializer(serializers.ModelSerializer):

    meeting_point_name = serializers.CharField(max_length=50, source='meeting_point.name', read_only=True)

    class Meta:
        model = Meeting
        exclude = ('user', 'status', 'is_validated', 'creation_date', 'last_update')


class MeetingSerializer(serializers.ModelSerializer):

    meeting_point_name = serializers.CharField(max_length=50, source='meeting_point.name', read_only=True)

    class Meta:
        model = Meeting
        read_only_fields = ('offer', 'user', 'is_validated', 'creation_date', 'last_update')
