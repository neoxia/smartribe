from rest_framework import serializers
from api.serializers import AddressSerializer
from core.models import Community, TransportStop, LocalCommunity, TransportCommunity


class CommunitySerializer(serializers.HyperlinkedModelSerializer):

    #type = serializers.CharField(source='get_type', read_only=True)

    class Meta:
        model = Community
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'last_update', 'auto_accept_member')
        read_only_fields = ('creation_date', 'last_update')


class LocalCommunitySerializer(serializers.HyperlinkedModelSerializer):

    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = LocalCommunity
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'last_update', 'auto_accept_member',
                  'address')
        read_only_fields = ('creation_date', 'last_update')


class TransportCommunitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransportCommunity
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'last_update', 'auto_accept_member',
                  'departure', 'via', 'arrival')
        read_only_fields = ('creation_date', 'last_update')


