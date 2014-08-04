from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action, link
from rest_framework.response import Response

from api.permissions.common import IsJWTAuthenticated
from api.permissions.community import IsCommunityOwner, IsCommunityModerator
from api.serializers.community import CommunityPublicSerializer
from api.serializers.member import MyMembersSerializer
from core.models import Community, Member
from api.serializers.serializers import CommunitySerializer, MemberSerializer
from api.authenticate import AuthUser


class CommunityViewSet(viewsets.ModelViewSet):
    """

    Inherits standard characteristics from ModelViewSet:

            | **Endpoint**: /communities/
            | **Methods**: GET / POST / PUT / PATCH / DELETE / OPTIONS
            | **Permissions**:
            |       - Default : IsCommunityOwner
            |       - GET or POST: IsJWTAuthenticated
            |       - PUT or PATCH : IsCommunityModerator

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

    def post_save(self, obj, created=False):
        # Retrieve request author and creates a member for him, as community owner
        user, _ = AuthUser().authenticate(self.request)
        owner = Member(user=user, community=obj, role="0", status="1")
        owner.save()

    # Simple user actions

    @action(methods=['POST', ], permission_classes=[IsJWTAuthenticated])
    def join_community(self, request, pk=None):
        """
        Become a new member of a community.

                | **permission**: JWTAuthenticated
                | **endpoint**: /communities/{id}/join_community/
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 201 Created
                |       - 401 Unauthorized
                | **data return**:
                |       None
                | **other actions**:
                |       None

        """
        user, _ = AuthUser().authenticate(request)
        if not Community.objects.filter(id=pk).exists():
            return Response({'detail': 'This community does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        community = Community.objects.get(id=pk)
        # Check if member already exists
        if Member.objects.filter(user=user, community=community).exists():
            member = Member.objects.get(user=user, community=community)
            return Response(MemberSerializer(member).data, status=status.HTTP_200_OK)
        # Defines the member, depending on auto_accept_member property of the community
        member = Member(user=user, community=community, role="2", status="0")
        if community.auto_accept_member:
            member.status = "1"
        # Register user as new member
        member.save(force_insert=True)
        return Response(status=status.HTTP_201_CREATED)

    @link(permission_classes=[IsJWTAuthenticated])
    def list_my_memberships(self, request, pk=None):
        """
        List the communities the authenticated user is member of.

                | **permission**: JWTAuthenticated
                | **endpoint**: /communities/0/list_my_memberships/
                | **method**: GET
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                | **data return**:
                |       - List of members objects :
                |           - community
                |               - url (string)
                |               - name (string)
                |               - description (text)
                |               - creation date (datetime)
                |           - status ('0', '1', '2')
                |           - role ('0', '1', '2')
                |           - registration_date (datetime)
                |           - last_modification_date (datetime)
                | **other actions**:
                |       None

        """
        user, _ = AuthUser().authenticate(request)
        my_members = Member.objects.filter(user=user)
        serializer = MyMembersSerializer(my_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['POST', ], permission_classes=[IsJWTAuthenticated])
    def leave_community(self, request, pk=None):
        """
        Leave a community.

                | **permission**: JWTAuthenticated
                | **endpoint**: /communities/{id}/leave_community/
                | **method**: POST
                | **attr**:
                |       None
                | **http return**:
                |       - 200 OK
                |       - 401 Unauthorized
                | **data return**:
                |       None
                | **other actions**:
                |       None
        """
        user, _ = AuthUser().authenticate(request)
        if not Community.objects.filter(id=pk).exists():
            return Response({'detail': 'This community does not exist'},
                            status=status.HTTP_400_BAD_REQUEST)
        community = Community.objects.get(id=pk)
        if not Member.objects.filter(user=user, community=community).exists():
            return Response({'detail': 'You are not a member of this community'},
                            status=status.HTTP_400_BAD_REQUEST)
        member = Member.objects.get(user=user, community=community)
        if member.status == '2':
            return Response({'detail': 'You have been banned from this community. You cannot leave it.'},
                            status=status.HTTP_401_UNAUTHORIZED)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Moderator actions
    def list_members(self):
        """
        List all members belonging to a community.
        """
        pass

    def accept_member(self):
        """
        Accept a membership request.
        """
        pass

    def ban_member(self):
        """
        Ban a member from community.
        """
        pass

    # Owner actions
    def promote_moderator(self):
        """
        Grant community moderator rights to a member.
        """
        pass
