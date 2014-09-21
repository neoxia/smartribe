from rest_framework import serializers
from api.serializers import AddressSerializer
from core.models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = Profile


class ProfileSerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = Profile
        read_only_fields = ('user', )
