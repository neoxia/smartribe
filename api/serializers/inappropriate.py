from rest_framework import serializers
from core.models import Inappropriate


class InappropriateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Inappropriate
        exclude = ('user', 'creation_date', 'last_update')