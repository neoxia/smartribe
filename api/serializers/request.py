from rest_framework import serializers
from core.models import Request


class RequestCreateSerializer(serializers.ModelSerializer):

     class Meta:
        model = Request


class RequestSerializer(serializers.ModelSerializer):

     class Meta:
        model = Request
        read_only_fields = ('user', 'creation_date')