from rest_framework import viewsets
from rest_framework.decorators import link
from rest_framework.response import Response
from api.authenticate import AuthUser
from api.permissions.common import IsJWTAuthenticated, IsJWTSelf, IsJWTOwner
from api.serializers import SkillCategorySerializer, SkillCreateSerializer, SkillSerializer

from core.models import Skill
from core.models.skill import SkillCategory
from rest_framework import mixins
from rest_framework import status


class SkillCategoryViewSet(viewsets.GenericViewSet,
                           mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           mixins.ListModelMixin):
    """
    Inherits standard characteristics from GenericViewSet and additionally provides
    'create', 'retrieve' and 'list' methods :
            | **Endpoint**: /skill_categories/
            | **Methods**: GET / POST / OPTIONS
            | **Permissions**:
            |       - Default : IsJWTAuthenticated
    """
    model = SkillCategory
    serializer_class = SkillCategorySerializer
    permission_classes = [IsJWTAuthenticated, ]
    filter_fields = ('user__id', )


class SkillViewSet(viewsets.ModelViewSet):
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

    def get_serializer_class(self):
        serializer_class = self.serializer_class
        if self.request.method == 'POST':
            serializer_class = SkillCreateSerializer
        return serializer_class

    def get_permissions(self):
        # TODO : Permissions must be different if pk or not
        if self.request.method == 'GET':
            return [IsJWTAuthenticated()]
        elif self.request.method == 'POST':
            return [IsJWTSelf()]
        else:
            return [IsJWTOwner()]

    @link()
    def list_my_skills(self, request, pk=None):
        """ """
        # TODO : Test
        user, _ = AuthUser().authenticate(self.request)
        my_skills = Skill.objects.filter(user=user)
        serializer = self.get_paginated_serializer(my_skills)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_paginated_serializer(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_pagination_serializer(page)
        else:
            serializer = self.get_serializer(queryset, many=True)
        return serializer
