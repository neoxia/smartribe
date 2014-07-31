from rest_framework import serializers
from core.models import Suggestion


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Suggestion
        fields = ('category', 'user', 'title', 'description')
