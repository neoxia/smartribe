from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Message


class MessageCreateSerializer(serializers.ModelSerializer):
    """  """

    class Meta:
        model = Message
        exclude = ('user', 'creation_date', )


class MessageSerializer(ReportableModelSerializer):
    """  """

    user_photo = serializers.CharField(source='get_photo', read_only=True)

    class Meta:
        model = Message
        read_only_fields = ('offer', 'user', 'creation_date')