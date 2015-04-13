from django.core.mail import send_mail

from api.permissions.common import IsJWTAuthenticated
from api.serializers.donation import DonationSerializer
from api.views.abstract_viewsets.custom_viewset import CreateOnlyViewSet
from core.models.donation import Donation


class DonationViewSet(CreateOnlyViewSet):
    """
    Inherits standard characteristics from CreateOnlyViewSet:

            | **Endpoint**: /donations/
            | **Methods**: POST
            | **Permissions**:
            |       - IsJWTAuthenticated

    """
    model = Donation
    serializer_class = DonationSerializer
    permission_classes = [IsJWTAuthenticated]

    def pre_save(self, obj):
        super().pre_save(obj)
        self.set_auto_user(obj)

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        message = 'Donor :\n' + obj.user.email \
                  + '\n\nDate   :\n' + str(obj.created_on) \
                  + '\n\nAmount :\n' + str(obj.amount) + ' €'

        send_mail('[SmarTribe] New donation',
                  message,
                  'donations@smartribe.fr',
                  ['contact@smartribe.fr'])
