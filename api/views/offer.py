from django.db.models import Q
from rest_framework.viewsets import ModelViewSet

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner
from api.permissions.offer import IsJWTSelfAndConcerned
from api.serializers import OfferSerializer, OfferCreateSerializer
from core.models import Offer


class OfferViewSet(ModelViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /offers/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTOwner
            |       - GET : IsJWTAuthenticated
            |       - POST : IsJWTSelfAndConcerned

    """
    model = Offer
    serializer_class = OfferSerializer
    filter_fields = ['request__user', 'request', 'user']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        if self.request.method == 'POST':
            return [IsJWTSelfAndConcerned()]
        return [IsJWTOwner()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = OfferCreateSerializer
        return serializer_class

    def pre_save(self, obj):
        user, _ = AuthUser().authenticate(self.request)
        if self.request.method == 'POST':
            obj.user = user

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return Offer.objects.filter(Q(user=user) | Q(request__user=user))
