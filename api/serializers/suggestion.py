from rest_framework import serializers
from core.models import FaqSection, Faq


class SuggestionSerializer(serializers.HyperlinkedModelSerializer):

    user = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Faq
        fields = ('category', 'user', 'title', 'description')
