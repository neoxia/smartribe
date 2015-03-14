from django.core.mail import send_mail
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from api.authenticate import AuthUser

from api.permissions.common import IsJWTSelf
from api.serializers.suggestion import SuggestionSerializer
from core.models import Suggestion


class SuggestionViewSet(CreateModelMixin, GenericViewSet):
    """
    Inherits standard characteristics from CreateModelMixin and GenericViewSet:

            | **Endpoint**: /suggestions/
            | **Methods**: POST
            | **Permissions**:
            |       - IsJWTSelf

    """
    model = Suggestion
    serializer_class = SuggestionSerializer
    permission_classes = [IsJWTSelf]

    def pre_save(self, obj):
        if self.request.method == 'POST':
            obj.user = self.request.user

    def post_save(self, obj, created=False):

        message = 'Category :\n' + obj.category \
                  + '\n\nReported by :\n' + obj.user.username \
                  + '\n\nTitle :\n' + obj.title \
                  + '\n\nDescription :\n' + obj.description

        send_mail('[SmarTribe] New suggestion',
                  message,
                  'noreply@smartribe.fr',
                  ['contact@smartribe.fr'])
