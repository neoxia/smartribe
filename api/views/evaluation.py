from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated
from api.permissions.evaluation import IsEvaluator
from api.serializers.evaluation import EvaluationSerializer, EvaluationCreateSerializer
from core.models import Evaluation


class EvaluationViewSet(ModelViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /evaluations/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsEvaluator
            |       - GET : IsJWTAuthenticated
            | **Notes**:
            |       - GET response restricted to 'Evaluation' objects linked with user

    """
    model = Evaluation
    serializer_class = EvaluationSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        return [IsEvaluator()]

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = EvaluationCreateSerializer
        return serializer_class

    def get_queryset(self):
        user, _ = AuthUser().authenticate(self.request)
        return self.model.objects.filter(Q(offer__user=user) |
                                         Q(offer__request__user=user))

    @link()
    def list_evaluations_about_me(self, request, pk=None):
        """
        List the evaluations created by other users about the authenticated user.

                | **permission**: JWTAuthenticated
                | **endpoint**: /evaluations/0/list_evaluations_about_me/
                | **method**: GET
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                | **data return**:
                |       - Count
                |       - List of "Evaluation" objects :
                |           - meeting (integer)
                |           - mark ('0'|'1'|'2'|'3'|'4'|'5')
                |           - comment (text)
                |           - creation_date (datetime)
                |           - last_update (datetime)
                | **other actions**:
                |       None

        """
        user, _ = AuthUser().authenticate(self.request)
        qs = self.get_queryset().filter(offer__user=user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @link()
    def list_evaluations_created_by_me(self, request, pk=None):
        """
        List the evaluations created by the user.

                | **permission**: JWTAuthenticated
                | **endpoint**: /evaluations/0/list_evaluations_created_by_me/
                | **method**: GET
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                |       - 403 Forbidden
                | **data return**:
                |       - Count
                |       - List of "Evaluation" objects :
                |           - meeting (integer)
                |           - mark ('0'|'1'|'2'|'3'|'4'|'5')
                |           - comment (text)
                |           - creation_date (datetime)
                |           - last_update (datetime)
                | **other actions**:
                |       None

        """
        user, _ = AuthUser().authenticate(self.request)
        qs = self.get_queryset().filter(offer__request__user=user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(self.object_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)