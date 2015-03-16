from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
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
        if isinstance(self.request.user, AnonymousUser):
            return Faq.objects.filter(private=False)
        return Faq.objects.all()
