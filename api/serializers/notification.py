from rest_framework import serializers
from core.models.notification import Notification


class NotificationSerializer(serializers.ModelSerializer):
    """ """

    class Meta:
        model = Notification
        read_only_fields = ['user', 'created_on']