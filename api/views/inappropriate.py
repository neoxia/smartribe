from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from api.permissions.common import IsJWTSelf
from api.serializers.inappropriate import InappropriateSerializer
from core.models import Inappropriate


class InappropriateViewSet(CreateModelMixin, GenericViewSet):
    """
    Inherits standard characteristics from CreateModelMixin and GenericViewSet:

            | **Endpoint**: /inappropriate/
            | **Methods**: POST
            | **Permissions**:
            |       - IsJWTSelf

    """
    model = Inappropriate
    serializer_class = InappropriateSerializer
    permission_classes = [IsJWTSelf]

    def post_save(self, obj, created=False):

        message = 'Reported by :\n' + obj.user.username \
                  + '\n\nContent URL :\n' + obj.content_url \
                  + '\n\nDetail :\n' + obj.detail

        send_mail('[SmarTribe] Inappropriate content report',
                  message,
                  'noreply@smartribe.fr',
                  ['contact@smartribe.fr'])
