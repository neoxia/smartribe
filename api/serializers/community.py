from rest_framework import serializers

from core.models import Community, LocalCommunity, TransportCommunity


class CommunitySerializer(serializers.ModelSerializer):

    type = serializers.CharField(max_length=1, source='get_type', read_only=True)

    members_count = serializers.IntegerField(source='get_members_count', read_only=True)

    class Meta:
        model = Community
        read_only_fields = ('creation_date', 'last_update')


class LocalCommunitySerializer(serializers.ModelSerializer):

    members_count = serializers.IntegerField(source='get_members_count', read_only=True)

    class Meta:
        model = LocalCommunity
        read_only_fields = ('creation_date', 'last_update')


class TransportCommunitySerializer(serializers.ModelSerializer):

    members_count = serializers.IntegerField(source='get_members_count', read_only=True)

    class Meta:
        model = TransportCommunity
        read_only_fields = ('creation_date', 'last_update')
