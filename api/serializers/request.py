from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Request


class RequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ('user', 'created_on', 'last_update')


class RequestSerializer(ReportableModelSerializer):

    user_username = serializers.CharField(max_length=255, source='user.username', read_only=True)

    user_first_name = serializers.CharField(max_length=255, source='user.first_name', read_only=True)

    user_last_name = serializers.CharField(max_length=255, source='user.last_name', read_only=True)

    class Meta:
        model = Request
        read_only_fields = ('user', 'created_on', 'last_update')