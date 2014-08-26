from rest_framework import serializers
from core.models import Meeting


class MeetingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting


class MeetingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Meeting
        read_only_fields = ('offer', 'creation_date', 'last_update')
