from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Offer


class OfferCreateSerializer(serializers.ModelSerializer):

    user_first_name = serializers.CharField(max_length=255, source='user.first_name', read_only=True)

    user_last_name = serializers.CharField(max_length=255, source='user.last_name', read_only=True)

    user_photo = serializers.CharField(source='get_photo', read_only=True)

    skill_title = serializers.CharField(source='get_skill_title', read_only=True)

    is_evaluated = serializers.BooleanField(source='is_evaluated', read_only=True)

    class Meta:
        model = Offer
        exclude = ('user', 'created_on', 'last_update')


class OfferSerializer(ReportableModelSerializer):

    user_first_name = serializers.CharField(max_length=255, source='user.first_name', read_only=True)

    user_last_name = serializers.CharField(max_length=255, source='user.last_name', read_only=True)

    user_photo = serializers.CharField(source='get_photo', read_only=True)

    skill_title = serializers.CharField(source='get_skill_title', read_only=True)

    is_evaluated = serializers.BooleanField(source='is_evaluated', read_only=True)

    class Meta:
        model = Offer
        read_only_fields = ('request', 'user', 'created_on', 'last_update', 'closed')