from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response
from rest_framework import status

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTSelf, IsJWTOwner
from api.serializers import RequestSerializer, RequestCreateSerializer
from core.models import Request, Member, Skill


class RequestViewSet(viewsets.ModelViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /requests/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTOwner
            |       - GET : IsJWTAuthenticated
            |       - POST : IsJWTSelf
            | **Notes**:
            |       - GET response restricted to 'Requests' objects linked with user and not closed

    """
    model = Request
    serializer_class = RequestSerializer
    filter_fields = ['user', 'category', 'closed']

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [IsJWTAuthenticated()]
        return [IsJWTOwner()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = RequestCreateSerializer
        return serializer_class

    def pre_save(self, obj):
        user, _ = AuthUser().authenticate(self.request)
        obj.user = user

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        my_communities = Member.objects.filter(user=user).values('community')
        linked_users = Member.objects.filter(community__in=my_communities).values('user')
        return self.model.objects.filter(Q(user__in=linked_users),
                                         Q(community=None) | Q(community__in=my_communities))

    def validate_object(self, request, pk):
        """  """
        if pk is None:
            return None, Response({'detail': 'Missing object index.'}, status=status.HTTP_400_BAD_REQUEST)
        if not self.model.objects.filter(id=pk).exists():
            return None, Response({'detail': 'This object does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        return self.model.objects.get(id=pk), None

    @link()
    def list_my_requests(self, request, pk=None):
        """
        List the requests created by the authenticated user.

                | **permission**: JWTAuthenticated
                | **endpoint**: /requests/0/list_my_requests/
                | **method**: GET
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                | **data return**:
                |       - List of request objects :
                |           - user (integer)
                |           - community (Community / Optional)
                |           - category (integer)
                |           - title (char 50)
                |           - detail (text)
                |           - creation_date (datetime)
                |           - expected_end_date (datetime)
                |           - end_date (datetime)
                |           - auto_close (boolean)
                |           - closed (boolean)
                | **other actions**:
                |       None

        """
        user, _ = AuthUser().authenticate(self.request)
        requests = self.model.objects.filter(user=user).order_by('-creation_date')
        serializer = self.get_paginated_serializer(requests)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @link()
    def list_suggested_requests_skills(self, request, pk=None):
        """  """
        user, _ = AuthUser().authenticate(self.request)
        my_category_list = Skill.objects.filter(user=user).values('category').distinct()


        queryset = self.get_queryset().exclude(user=user).filter(category__in=my_category_list).order_by('-creation_date')
        serializer = self.get_paginated_serializer(queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_paginated_serializer(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return serializer


    @action()
    def close_request(self, request, pk=None):
        """
        Close a request.

                | **permission**: IsJWTOwner
                | **endpoint**: /requests/{id}/close_request/
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                | **data return**:
                |       - Modified request object
                | **other actions**:
                |       None

        """
        req, response = self.validate_object(request, pk)
        if not req:
            return response
        user, _ = AuthUser().authenticate(request)
        if req.user != user:
            return Response({'detail': 'Operation not allowed.'}, status.HTTP_403_FORBIDDEN)
        req.closed = True
        req.save()
        serializer = RequestSerializer(req)
        return Response(serializer.data, status=status.HTTP_200_OK)
