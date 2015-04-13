from rest_framework import serializers
from core.models.donation import Donation


class DonationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Donation
        read_only_fields = ('user', 'created_on')
