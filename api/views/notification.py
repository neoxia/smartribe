from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner
from api.serializers.notification import NotificationSerializer
from core.models.notification import Notification


class NotificationViewSet(mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """ """
    model = Notification
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsJWTOwner()]

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return self.model.objects.filter(user=user).order_by('created_on')
