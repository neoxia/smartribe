from rest_framework import serializers
from api.serializers import AddressSerializer
from core.models import Profile


class ProfileCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = Profile
        fields = ('url', 'user', 'gender', 'address', 'phone', 'birthdate', 'bio', 'photo', 'favorite_contact')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    address = AddressSerializer(many=False, blank=True)

    class Meta:
        model = Profile
        fields = ('url', 'user', 'gender', 'address', 'phone', 'birthdate', 'bio', 'photo', 'favorite_contact')
        read_only_fields = ('user',)