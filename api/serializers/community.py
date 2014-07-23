from rest_framework import serializers
from api.serializers import AddressSerializer
from core.models import LocalCommunity, TransportCommunity


class LocalCommunitySerializer(serializers.HyperlinkedModelSerializer):

    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = LocalCommunity
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'auto_accept_member',
                  'address')
        read_only_fields = ('creation_date',)


class TransportCommunitySerializer(serializers.HyperlinkedModelSerializer):

    transport_stop_departure = serializers.PrimaryKeyRelatedField()
    transport_stop_via = serializers.PrimaryKeyRelatedField()
    transport_stop_arrival = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = TransportCommunity
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'auto_accept_member',
                  'transport_stop_departure', 'transport_stop_via', 'transport_stop_arrival')
        read_only_fields = ('creation_date',)


class TransportStopSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransportCommunity
        fields = ('url', 'id',
                  'name', 'detail')
