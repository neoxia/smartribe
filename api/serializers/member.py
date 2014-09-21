from rest_framework import serializers
from api.serializers import UserPublicSerializer
from api.serializers.community import CommunitySerializer
from core.models import Member


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        read_only_fields = ('user', 'community', 'registration_date')


class MyMembersSerializer(serializers.ModelSerializer):

    community = CommunitySerializer()

    class Meta:
        model = Member
        #fields = ('community', 'role', 'status', 'registration_date', 'last_modification_date')
        exclude = ('user', )


class ListCommunityMembersSerializer(serializers.ModelSerializer):

    user = UserPublicSerializer()

    class Meta:
        model = Member
        #fields = ('id', 'user', 'role', 'status', 'registration_date', 'last_modification_date')
        exclude = ('community', )
