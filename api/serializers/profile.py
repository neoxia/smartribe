from rest_framework import serializers
from api.serializers import AddressSerializer
from core.models import Profile


class ProfileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        read_only_fields = ('user', )
