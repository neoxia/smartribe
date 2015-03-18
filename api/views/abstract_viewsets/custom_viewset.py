from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.viewsets import ModelViewSet


class LoggingComponent(object):

    def post_save(self, view, obj, created=False):
        create = False
        if view.request.method == 'POST':
            create = True
        self.log(view, obj, ADDITION if create else CHANGE)

    former_id = None

    def pre_delete(self, obj):
        self.former_id = obj.id

    def post_delete(self, view, obj):
        self.log(obj, DELETION, self.former_id)

    def log(self, view, obj, flag, id=None, change_message=""):
        if id is None:
            id = obj.id
        LogEntry.objects.log_action(user_id=view.request.user.id,
                                    content_type_id=ContentType.objects.get_for_model(view.model).pk,
                                    object_id=id,
                                    object_repr=str(obj),
                                    action_flag=flag,
                                    change_message=change_message)


class CreationComponent(object):

    def set_auto_user(self, view, obj):
        if view.request.method == 'POST':
            obj.user = view.request.user

class CreateOnlyGenericViewSet(mixins.CreateModelMixin, GenericViewSet):
    """ Not intended to be used directly """


class CreateOnlyViewSet(CreateOnlyGenericViewSet):

    _logging = LoggingComponent()
    _creation = CreationComponent()

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        self._logging.post_save(self, obj, created)

    def log(self, obj, flag, id=None, change_message=""):
        self._logging.log(self, obj, flag, id, change_message)

    def set_auto_user(self, obj):
        self._creation.set_auto_user(self, obj)


class CreateAndReadOnlyGenericViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                                      mixins.ListModelMixin, GenericViewSet):
    """ Not intended to be used directly """


class CreateAndReadOnlyViewSet(CreateAndReadOnlyGenericViewSet):

    _logging = LoggingComponent()
    _creation = CreationComponent()

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        self._logging.post_save(self, obj, created)

    def pre_delete(self, obj):
        super().pre_delete(obj)
        self._logging.pre_delete(obj)

    def post_delete(self, obj):
        super().post_delete(obj)
        self._logging.post_delete(self, obj)

    def log(self, obj, flag, id=None, change_message=""):
        self._logging.log(self, obj, flag, id, change_message)

    def set_auto_user(self, obj):
        self._creation.set_auto_user(self, obj)


class ReadAndDestroyGenericViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                                   GenericViewSet):
    """ Not intended to be used directly """


class ReadAndDestroyViewSet(ReadAndDestroyGenericViewSet):

    _logging = LoggingComponent()

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        self._logging.post_save(self, obj, created)

    def pre_delete(self, obj):
        super().pre_delete(obj)
        self._logging.pre_delete(obj)

    def post_delete(self, obj):
        super().post_delete(obj)
        self._logging.post_delete(self, obj)

    def log(self, obj, flag, id=None, change_message=""):
        self._logging.log(self, obj, flag, id, change_message)


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
        data = request.DATA
        if request.method == 'GET':
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
        if self.request.method == 'POST':
            obj.user = self.request.user

    def get_paginated_serializer(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return serializer

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        create = False
        if self.request.method == 'POST':
            create = True
        self.log(obj, ADDITION if create else CHANGE)

    former_id = None

    def pre_delete(self, obj):
        super().pre_delete(obj)
        self.former_id = obj.id

    def post_delete(self, obj):
        super().post_delete(obj)
        self.log(obj, DELETION, self.former_id)

    def log(self, obj, flag, id=None, change_message=""):
        if id is None:
            id = obj.id
        LogEntry.objects.log_action(user_id=self.request.user.id,
                                    content_type_id=ContentType.objects.get_for_model(self.model).pk,
                                    object_id=id,
                                    object_repr=str(obj),
                                    action_flag=flag,
                                    change_message=change_message)

    class Meta:
        abstract = True