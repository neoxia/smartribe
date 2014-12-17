from rest_framework import serializers
from api.serializers import ReportableModelSerializer
from core.models import Message


class MessageCreateSerializer(serializers.ModelSerializer):
    """  """

    user_first_name = serializers.CharField(max_length=255, source='user.first_name', read_only=True)

    user_last_name = serializers.CharField(max_length=255, source='user.last_name', read_only=True)

    user_photo = serializers.CharField(source='get_photo', read_only=True)

    class Meta:
        model = Message
        exclude = ('user', 'creation_date', )


class MessageSerializer(ReportableModelSerializer):
    """  """

    user_first_name = serializers.CharField(max_length=255, source='user.first_name', read_only=True)

    user_last_name = serializers.CharField(max_length=255, source='user.last_name', read_only=True)

    user_photo = serializers.CharField(source='get_photo', read_only=True)

    class Meta:
        model = Message
        read_only_fields = ('offer', 'user', 'creation_date')