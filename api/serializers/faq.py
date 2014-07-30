from rest_framework import serializers
from core.models import FaqSection, Faq


class FaqSectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = FaqSection
        fields = ('title', )


class FaqSerializer(serializers.HyperlinkedModelSerializer):

    section = FaqSectionSerializer()

    class Meta:
        model = Faq
        fields = ('section', 'question', 'answer')
