from rest_framework import serializers
from api.serializers import UserPublicSerializer
from api.serializers.community import CommunitySerializer
from core.models import Member


class MemberCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('id', 'user', 'community')


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        read_only_fields = ('user', 'community', 'registration_date')


class MyMembersSerializer(serializers.HyperlinkedModelSerializer):

    community = CommunitySerializer()

    class Meta:
        model = Member
        fields = ('community', 'role', 'status', 'registration_date', 'last_modification_date')

class ListCommunityMemberSerializer(serializers.HyperlinkedModelSerializer):

    user = UserPublicSerializer()

    class Meta:
        model = Member
        fields = ('id', 'user', 'role', 'status', 'registration_date', 'last_modification_date')