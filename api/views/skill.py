from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework import status

from api.permissions.common import IsJWTAuthenticated, IsJWTSelf, IsJWTOwner
from api.serializers import SkillCreateSerializer, SkillSerializer
from api.views.abstract_viewsets.custom_viewset import CustomViewSet
from core.models import Skill


class SkillViewSet(CustomViewSet):
    """
    Inherits standard characteristics from ModelViewSet:
            | **Endpoint**: /skills/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTOwner
            |       - GET : IsJWTAuthenticated
            |       - POST : IsJWTSelf
    """
    model = Skill
    serializer_class = SkillSerializer
    filter_fields = ('user__id', 'category__id')

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = SkillCreateSerializer
        return serializer_class

    def get_permissions(self):
        # TODO : Permissions must be different if pk or not
        if self.request.method in ['GET', 'POST']:
            return [IsJWTAuthenticated()]
        else:
            return [IsJWTOwner()]

    def pre_save(self, obj):
        super().pre_save(obj)
        self.set_auto_user(obj)

    @link()
    def list_my_skills(self, request, pk=None):
        """ """
        my_skills = Skill.objects.filter(user=self.request.user)
        serializer = self.get_paginated_serializer(my_skills)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_paginated_serializer(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return serializer
