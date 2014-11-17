from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers



def validate_email_unique(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Email address %s already exists, must be unique' % value)


class UserCreateSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True, validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_active')
        write_only_fields = ('password', )
        exclude = ('groups', )


class UserPublicSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        read_only_fields = ('username', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'groups')
        read_only_fields = ('username', 'email')
        write_only_fields = ('password', )
