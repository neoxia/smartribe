from django.core.mail import send_mail
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin
from api.permissions.common import IsJWTAuthenticated
from api.serializers.faq import FaqSerializer
from api.serializers.suggestion import SuggestionSerializer
from core.models import Faq, Suggestion


class SuggestionViewSet(CreateModelMixin, GenericViewSet):
    """
    Inherits standard characteristics from CreateModelMixin and GenericViewSet:

            | **Endpoint**: /suggestions/
            | **Methods**: GET
            | **Permissions**:
            |       - AllowAny : Public questions
            |       - IsJWTAuthenticated : All questions


    """
    model = Suggestion
    serializer_class = SuggestionSerializer
    permission_classes = [IsJWTAuthenticated]

    def post_save(self, obj, created=False):

        message = 'Category :\n' + obj.category \
                  + '\n\nReported by :\n' + obj.user.username \
                  + '\n\nTitle :\n' + obj.title \
                  + '\n\nDescription :\n' + obj.description

        send_mail('[SmarTribe] New suggestion',
                  message,
                  'noreply@smartribe.fr',
                  ['admin@smartribe.fr'])
