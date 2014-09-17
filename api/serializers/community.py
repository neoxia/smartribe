from rest_framework import serializers
from api.serializers.address import AddressSerializer
from core.models import Community, LocalCommunity, TransportCommunity


class CommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Community
        read_only_fields = ('creation_date', 'last_update')


class LocalCommunitySerializer(serializers.ModelSerializer):

    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = LocalCommunity
        read_only_fields = ('creation_date', 'last_update')


class TransportCommunitySerializer(serializers.ModelSerializer):

    class Meta:
        model = TransportCommunity
        read_only_fields = ('creation_date', 'last_update')
