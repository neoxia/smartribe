from rest_framework import serializers
from core.models import FaqSection, Faq


class FaqSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FaqSection


class FaqSerializer(serializers.ModelSerializer):

    section = FaqSectionSerializer()

    class Meta:
        model = Faq
        exclude = ('private', 'creation_date', 'last_update')
