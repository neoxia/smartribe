from rest_framework import viewsets
from api.permissions.common import IsJWTAuthenticated, IsJWTSelf, IsJWTOwner

from api.serializers.serializers import SkillSerializer, SkillCategorySerializer, SkillCreateSerializer
from core.models import Skill
from core.models.skill import SkillCategory
from rest_framework import mixins


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
        if self.request.method == 'GET' and not 'pk' in self.kwargs:
            return [IsJWTAuthenticated()]
        elif self.request.method == 'POST':
            return [IsJWTSelf()]
        else:
            return [IsJWTOwner()]
