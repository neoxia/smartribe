from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Request


class RequestCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        exclude = ('user', 'created_on', 'last_update')


class RequestSerializer(ReportableModelSerializer):

    class Meta:
        model = Request
        read_only_fields = ('user', 'created_on', 'last_update')