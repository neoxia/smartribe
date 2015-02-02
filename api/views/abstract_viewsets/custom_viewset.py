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

    @staticmethod
    def validate_external_object(object_class, field_name, request):
        """  """
        data = request.QUERY_PARAMS
        if not field_name in data:
            return None, Response({'detail': 'Missing \'' + field_name + '\' in query parameters.'},
                                  status=status.HTTP_400_BAD_REQUEST)
        if data[field_name] is None:
            return None, Response({'detail': 'Missing object index.'}, status=status.HTTP_400_BAD_REQUEST)
        if not object_class.objects.filter(id=data[field_name]).exists():
            return None, Response({'detail': 'This object does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return object_class.objects.get(id=data[field_name]), None

    def set_auto_user(self, obj):
        user, _ = AuthUser().authenticate(self.request)
        if self.request.method == 'POST':
            obj.user = user

    def get_paginated_serializer(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return serializer

    class Meta:
        abstract = True