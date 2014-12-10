from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from api.authenticate import AuthUser


class CustomViewSet(ModelViewSet):
    """ """

    create_serializer_class = None

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class
        return self.serializer_class

    def validate_object(self, request, pk):
        """  """
        if pk is None:
            return None, Response({'detail': 'Missing object index.'}, status=status.HTTP_400_BAD_REQUEST)
        if not self.model.objects.filter(id=pk).exists():
            return None, Response({'detail': 'This object does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return self.model.objects.get(id=pk), None

    def set_auto_user(self, obj):
        user, _ = AuthUser().authenticate(self.request)
        if self.request.method == 'POST':
            obj.user = user

    class Meta:
        abstract = True