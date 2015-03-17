from django.contrib.admin.models import CHANGE
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.permissions.common import IsJWTAuthenticated, IsJWTOwner
from api.serializers.notification import NotificationSerializer
from api.views.abstract_viewsets.custom_viewset import ReadAndDestroyViewSet
from core.models.notification import Notification


class NotificationViewSet(ReadAndDestroyViewSet):
    """ """
    model = Notification
    serializer_class = NotificationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsJWTOwner()]

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('created_on')

    @action()
    def tag_as_seen(self, request, pk=None):
        """ """
        if pk is None:
            return Response({'detail': 'Missing object index.'}, status=status.HTTP_400_BAD_REQUEST)
        if not self.model.objects.filter(id=pk).exists():
            return Response({'detail': 'This object does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        n = self.model.objects.get(id=pk)
        n.seen = True
        n.seen_on = timezone.now()
        n.save()
        serializer = self.serializer_class(n, many=False)
        self.log(n, CHANGE, None, "Tagged as seen")
        return Response(serializer.data, status=status.HTTP_200_OK)