from django.contrib.auth.models import User
from rest_framework import serializers


class UserCreateSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups', 'is_active')
        write_only_fields = ('password',)


class UserPublicSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'id')
        read_only_fields = ('username',)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'groups')
        read_only_fields = ('username',)
        write_only_fields = ('password',)
