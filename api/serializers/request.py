from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Request


class RequestCreateSerializer(ReportableModelSerializer):

    user_first_name = serializers.CharField(max_length=255, source='user.first_name', read_only=True)

    user_last_name = serializers.CharField(max_length=255, source='user.last_name', read_only=True)

    user_photo = serializers.CharField(source='get_photo', read_only=True)

    user_is_donor = serializers.BooleanField(source='user.profile.is_donor', read_only=True)

    user_is_early_adopter = serializers.BooleanField(source='user.profile.is_early_adopter', read_only=True)

    community_name = serializers.CharField(max_length=255, source='community.name', read_only=True)

    category_name = serializers.CharField(max_length=255, source='category.name', read_only=True)

    offers_count = serializers.IntegerField(source='get_offers_count', read_only=True)

    class Meta:
        model = Request
        exclude = ('user', 'created_on', 'last_update')


class RequestSerializer(RequestCreateSerializer):

    class Meta:
        model = Request
        read_only_fields = ('user', 'created_on', 'last_update')