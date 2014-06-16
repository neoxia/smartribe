from django.contrib.auth.models import User, Group, Permission
from rest_framework.authtoken.models import Token
from core.models import Profile, Skill, Community, Request, Offer, Member
from rest_framework import serializers


# USER

class UserCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups')
        write_only_fields = ('password',)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups')
        read_only_fields = ('username',)
        write_only_fields = ('password',)


# GROUP

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name', 'permissions')


# TOKEN

class TokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Token
        fields = ('user', 'key')


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ('url', 'name', 'codename')


# PROFILE

class ProfileCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Profile
        fields = ('url', 'user', 'gender', 'birthdate', 'bio', 'photo')


class ProfileSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Profile
        fields = ('url', 'user', 'gender', 'birthdate', 'bio', 'photo')
        read_only_fields = ('user',)


# SKILL

class SkillSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Skill
        fields = ('user', 'description')


# COMMUNITY

class CommunityCreateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Community
        fields = ('url', 'name', 'description', 'creation_date', 'auto_accept_member')

class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Community
        fields = ('url', 'name', 'description', 'creation_date', 'auto_accept_member')


# MEMBER

class MemberCreateSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField()
    community = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Member
        fields = ('url', 'user', 'community', 'status', 'registration_date', 'last_modification_date')

class MemberSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Member
        fields = ('url', 'user', 'community', 'status', 'registration_date', 'last_modification_date')
        read_only_fields = ('user','community', 'registration_date')


# REQUEST

class RequestSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Request
        fields = ('user', 'title', 'description')


class OfferSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Offer
        fields = ('request', 'description')
