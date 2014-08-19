from rest_framework import serializers
from core.models import Location


class LocationCreateSerializer(serializers.ModelSerializer):
    """
    Location create serializer
    """
    #community = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Location


class LocationSerializer(serializers.ModelSerializer):
    """
    Location standard serializer
    """

    class Meta:
        model = Location
        read_only_fields = ('community', )