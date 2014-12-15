from rest_framework import viewsets, mixins
from api.permissions.common import IsJWTAuthenticated
from api.serializers import SkillCategorySerializer
from core.models import SkillCategory

__author__ = 'Renaud'


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