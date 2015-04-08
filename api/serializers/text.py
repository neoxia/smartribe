from rest_framework import serializers
from core.models.text import Text


class TextSerializer(serializers.ModelSerializer):

    class Meta:
        model = Text
        fields = ('content', )
