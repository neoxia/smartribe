from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from api.permissions.common import IsJWTAuthenticated
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
    permission_classes = [IsJWTAuthenticated]

    def pre_save(self, obj):
        if self.request.method == 'POST':
            obj.user = self.request.user

    def post_save(self, obj, created=False):

        message = 'Reported by :\n' + obj.user.email \
                  + '\n\nTarget content :\n' + obj.content_identifier \
                  + '\n\nDetail :\n' + obj.detail

        send_mail('[SmarTribe] Inappropriate content report',
                  message,
                  'noreply@smartribe.fr',
                  ['contact@smartribe.fr'])
