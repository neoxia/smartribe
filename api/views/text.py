from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from api.serializers.text import TextSerializer
from core.models.text import Text


class TextViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Inherits standard characteristics from ReadOnlyModelViewSet:

            | **Endpoint**: /texts/
            | **Methods**: GET
            | **Permissions**:
            |       - AllowAny : Public texts
            |       - IsJWTAuthenticated : All texts

    """
    model = Text
    serializer_class = TextSerializer
    permission_classes = [AllowAny]

    filter_fields = ('tag', )
    lookup_field = "tag"


    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return Text.objects.filter(private=False)
        return Text.objects.all()
