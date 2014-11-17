from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Offer


class OfferCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Offer
        exclude = ('user', 'created_on', 'last_update')


class OfferSerializer(ReportableModelSerializer):

    class Meta:
        model = Offer
        read_only_fields = ('request', 'user', 'created_on', 'last_update')