from rest_framework import serializers
from core.models import Meeting


class MeetingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        exclude = ('user', 'status', 'is_validated', 'creation_date', 'last_update')


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        read_only_fields = ('offer', 'user', 'is_validated', 'creation_date', 'last_update')
