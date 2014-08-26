from rest_framework import serializers
from core.models import MeetingPoint


class MeetingPointCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingPoint


class MeetingPointSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeetingPoint
        read_only_fields = ('location', )
