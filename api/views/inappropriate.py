from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from api.permissions.common import IsJWTAuthenticated
from api.serializers.inappropriate import InappropriateSerializer
from api.views.abstract_viewsets.custom_viewset import LoggingComponent, CreateOnlyViewSet
from core.models import Inappropriate


class InappropriateViewSet(CreateOnlyViewSet):
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
        super().pre_save(obj)
        self.set_auto_user(obj)

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        message = 'Reported by :\n' + obj.user.email \
                  + '\n\nTarget content :\n' + obj.content_identifier \
                  + '\n\nDetail :\n' + obj.detail

        send_mail('[SmarTribe] Inappropriate content report',
                  message,
                  'noreply@smartribe.fr',
                  ['contact@smartribe.fr'])
