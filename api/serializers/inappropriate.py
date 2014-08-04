from rest_framework import serializers
from core.models import Inappropriate


class InappropriateSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Inappropriate
        fields = ('user', 'content_url', 'detail')
