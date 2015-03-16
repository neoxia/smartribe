from rest_framework import serializers
from core.models import Suggestion


class SuggestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Suggestion
        exclude = ('user', 'creation_date', 'last_update')
