from rest_framework import viewsets
from rest_framework.decorators import link, action
from rest_framework.response import Response
from rest_framework import status

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTSelf, IsJWTOwner
from api.serializers import RequestSerializer, RequestCreateSerializer
from core.models import Request, Member


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

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        if self.request.method == 'POST' and 'pk' not in self.kwargs:
            return [IsJWTSelf()]
        return [IsJWTOwner()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = RequestCreateSerializer
        return serializer_class

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        my_communities = Member.objects.filter(user=user).values('community')
        linked_users = Member.objects.filter(community__in=my_communities).values('user')
        return self.model.objects.filter(user__in=linked_users)

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
        requests = self.model.objects.filter(user=user)
        page = self.paginate_queryset(requests)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(permission_classes=[IsJWTOwner])
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
        user, _ = AuthUser().authenticate(request)
        if pk is None:
            return Response({'detail': 'Id requested in URL.'}, status.HTTP_404_NOT_FOUND)
        if not self.model.objects.filter(id=pk).exists():
            return Response({'detail': 'No such object.'}, status.HTTP_404_NOT_FOUND)
        req = self.model.objects.get(id=pk)
        if req.user != user:
            return Response({'detail': 'Operation not allowed.'}, status.HTTP_403_FORBIDDEN)
        req.closed = True
        req.save()
        serializer = RequestSerializer(req)
        return Response(serializer.data, status=status.HTTP_200_OK)
