from django.db.models import Q

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner
from api.permissions.offer import IsJWTSelfAndConcerned
from api.serializers import OfferSerializer, OfferCreateSerializer
from api.views.abstract_viewsets.custom_viewset import CustomViewSet
from core.models import Offer


class OfferViewSet(CustomViewSet):
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
    create_serializer_class = OfferCreateSerializer
    serializer_class = OfferSerializer
    filter_fields = ['request__user__id', 'request__id', 'user__id']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        if self.request.method == 'POST':
            return [IsJWTSelfAndConcerned()]
        return [IsJWTOwner()]

    def pre_save(self, obj):
        self.set_auto_user(obj)

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return Offer.objects.filter(Q(user=user) | Q(request__user=user))
