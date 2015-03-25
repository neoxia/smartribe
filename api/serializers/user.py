from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.contrib.auth import get_user_model



class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password', 'is_active')
        write_only_fields = ('password', )
        exclude = ('groups', )


class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'groups', 'last_login')
        read_only_fields = ('email', 'last_login')
        write_only_fields = ('password', )
