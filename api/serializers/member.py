from rest_framework import serializers
from api.serializers import UserPublicSerializer
from api.serializers.community import CommunityPublicSerializer
from core.models import Member


class MemberCreateSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField()
    community = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Member
        fields = ('url', 'user', 'community')


class MemberSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Member
        fields = ('url', 'user', 'community', 'role', 'status', 'registration_date', 'last_modification_date')
        read_only_fields = ('user', 'community', 'registration_date')


class MyMembersSerializer(serializers.HyperlinkedModelSerializer):

    community = CommunityPublicSerializer()

    class Meta:
        model = Member
        fields = ('community', 'role', 'status', 'registration_date', 'last_modification_date')

class ListCommunityMemberSerializer(serializers.HyperlinkedModelSerializer):

    user = UserPublicSerializer()

    class Meta:
        model = Member
        fields = ('id', 'user', 'role', 'status', 'registration_date', 'last_modification_date')