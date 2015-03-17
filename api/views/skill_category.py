from rest_framework.decorators import link
from rest_framework.response import Response
from rest_framework import status
from api.permissions.common import IsJWTAuthenticated
from api.serializers import SkillCategorySerializer
from api.views.abstract_viewsets.custom_viewset import CreateAndReadOnlyViewSet
from core.models import SkillCategory, Community, Member, Skill


class SkillCategoryViewSet(CreateAndReadOnlyViewSet):
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

    @link()
    def list_members_skill_categories(self, request, pk=None):
        """ """
        community, response = self.validate_external_object(Community, 'community', request)
        if not community:
            return response
        members = Member.objects.filter(community=community, status='1').values('user')
        skills = Skill.objects.filter(user__in=members)

    # /////////////
    # /// Tools ///
    # /////////////

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