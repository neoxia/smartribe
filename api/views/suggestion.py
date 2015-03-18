from django.core.mail import send_mail

from api.permissions.common import IsJWTAuthenticated
from api.serializers.suggestion import SuggestionSerializer
from api.views.abstract_viewsets.custom_viewset import CreateOnlyViewSet
from core.models import Suggestion


class SuggestionViewSet(CreateOnlyViewSet):
    """
    Inherits standard characteristics from CreateModelMixin and GenericViewSet:

            | **Endpoint**: /suggestions/
            | **Methods**: POST
            | **Permissions**:
            |       - IsJWTSelf

    """
    model = Suggestion
    serializer_class = SuggestionSerializer
    permission_classes = [IsJWTAuthenticated]

    def pre_save(self, obj):
        super().pre_save(obj)
        self.set_auto_user(obj)

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        message = 'Category :\n' + obj.get_category_display() \
                  + '\n\nReported by :\n' + obj.user.email \
                  + '\n\nTitle :\n' + obj.title \
                  + '\n\nDescription :\n' + obj.description

        send_mail('[SmarTribe] New suggestion',
                  message,
                  'suggestions@smartribe.fr',
                  ['contact@smartribe.fr'])
