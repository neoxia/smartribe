from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from api.permissions.common import IsJWTAuthenticated
from api.permissions.community import IsCommunityOwner, IsCommunityModerator
from core.models import Community, Member
from api.serializers.serializers import CommunitySerializer
from api.authenticate import AuthUser


class CommunityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows communities to be viewed or edited.
    """
    model = Community
    serializer_class = CommunitySerializer
    def get_permissions(self):
        """
        An authenticated user can create a new community or see existing communities.
        Only owner or moderator can modify an existing community.
        """
        if self.request.method == 'GET' or self.request.method == 'POST':
            return [IsJWTAuthenticated()]
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            return [IsCommunityModerator()]
        else:
            return [IsCommunityOwner()]

    def create(self, request, *args, **kwargs):
        """ Create community:

                | **permission**: authenticated
                | **endpoint**: /communities/
                | **method**: POST
                | **attr**:
                |       - name: string (required)
                |       - description: string (required)
                |       - auto_accept_member: boolean (true|false)
                | **http return**:
                |       - 201 Created on success
                |       - 400 Bad request on error
                | **data return**:
                |       - url: ressource
                |       - name: string
                |       - description: string
                |       - created_date : date
                |       - auto_accept_member: boolean (true|false)

        """
        serializer = self.get_serializer(data=request.DATA, files=request.FILES)

        if serializer.is_valid():
            self.pre_save(serializer.object)
            self.object = serializer.save(force_insert=True)
            self.post_save(self.object, created=True)
            headers = self.get_success_headers(serializer.data)
            # Retrieve request author and creates him a member as community owner
            user, _ = AuthUser().authenticate(request)
            owner = Member(user=user, community=self.object, role="0", status="1")
            owner.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
