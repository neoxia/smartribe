from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import link
from rest_framework.response import Response

from api.permissions.common import IsJWTAuthenticated
from api.permissions.evaluation import IsEvaluator, IsEvaluationAuthor
from api.serializers.evaluation import EvaluationSerializer, EvaluationCreateSerializer
from api.views.abstract_viewsets.custom_viewset import CustomViewSet
from core.models import Evaluation


class EvaluationViewSet(CustomViewSet):
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
    create_serializer_class = EvaluationCreateSerializer
    serializer_class = EvaluationSerializer
    filter_fields = ('offer__id', 'usefull')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        if self.request.method == 'POST':
            return [IsEvaluator()]
        return [IsEvaluationAuthor()]

    def post_save(self, obj, created=False):
        super().post_save(obj, created)
        obj.offer.closed = True
        obj.offer.save()

    def get_queryset(self):
        return self.model.objects.filter(Q(offer__user=self.request.user) |
                                         Q(offer__request__user=self.request.user))

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
        qs = self.get_queryset().filter(offer__user=self.request.user)
        serializer = self.get_paginated_serializer(qs)
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
        qs = self.get_queryset().filter(offer__request__user=self.request.user)
        serializer = self.get_paginated_serializer(qs)
        return Response(serializer.data, status=status.HTTP_200_OK)