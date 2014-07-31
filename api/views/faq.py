from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.serializers.faq import FaqSerializer
from core.models import Faq


class FaqViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Inherits standard characteristics from ReadOnlyModelViewSet:

            | **Endpoint**: /faq/
            | **Methods**: GET
            | **Permissions**:
            |       - AllowAny : Public questions
            |       - IsJWTAuthenticated : All questions


    """
    model = Faq
    serializer_class = FaqSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        if user is not None:
            return Faq.objects.all()
        return Faq.objects.filter(private=False)
