from rest_framework import serializers
from api.serializers import AddressSerializer
from core.models import Community, TransportStop, LocalCommunity, TransportCommunity


class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Community
        fields = ('url', 'name', 'description', 'creation_date', 'last_update', 'auto_accept_member')
        read_only_fields = ('creation_date', 'last_update')


class CommunityPublicSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Community
        fields = ('url', 'name', 'description', 'creation_date', 'last_update')
        read_only_fields = ('creation_date', 'last_update')


class LocalCommunitySerializer(serializers.HyperlinkedModelSerializer):

    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = LocalCommunity
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'last_update', 'auto_accept_member',
                  'address')
        read_only_fields = ('creation_date', 'last_update')


class TransportStopSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TransportStop
        fields = (#'url', 'id',
                  'name', 'detail')



class TransportCommunitySerializer(serializers.HyperlinkedModelSerializer):

    #transport_stop_departure = serializers.PrimaryKeyRelatedField()
    #transport_stop_via = serializers.PrimaryKeyRelatedField()
    #transport_stop_arrival = serializers.PrimaryKeyRelatedField()

    #transport_stop_departure = TransportStopSerializer(many=False)
    #transport_stop_via = TransportStopSerializer(many=False)
    #transport_stop_arrival = TransportStopSerializer(many=False)

    class Meta:
        model = TransportCommunity
        fields = ('url', 'id',
                  'name', 'description', 'creation_date', 'last_update', 'auto_accept_member',
                  'departure', 'via', 'arrival')
        read_only_fields = ('creation_date', 'last_update')


